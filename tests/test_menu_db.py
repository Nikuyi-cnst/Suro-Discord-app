import os
import tempfile
import types
import unittest
from pathlib import Path
from typing import cast
from unittest.mock import AsyncMock, patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import Index


class MenuDbTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "menus.db"
        Index.MENU_DB_FILE = self.db_path

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_delete_menu_respects_owner_and_admin(self):
        Index.initialize_menu_db()
        self.assertTrue(Index.add_menu(1, "짜장면", 101))
        self.assertTrue(Index.add_menu(1, "짬뽕", 102))

        self.assertTrue(Index.delete_menu(1, "짜장면", 101, is_admin=False))
        self.assertFalse(Index.delete_menu(1, "짬뽕", 101, is_admin=False))
        self.assertTrue(Index.delete_menu(1, "짬뽕", 999, is_admin=True))

        remaining = Index.get_menu_entries(1)
        self.assertEqual(remaining, [])

    def test_menu_admin_list_allows_special_admins(self):
        old_value = os.environ.get("ADMIN_IDS")
        os.environ["ADMIN_IDS"] = "9001, 9002"
        try:
            self.assertTrue(Index.is_menu_admin(types.SimpleNamespace(id=9001)))# type: ignore
            self.assertTrue(Index.is_menu_admin(types.SimpleNamespace(id=9002)))# type: ignore
            self.assertFalse(Index.is_menu_admin(types.SimpleNamespace(id=1234)))# type: ignore
        finally:
            if old_value is None:
                os.environ.pop("ADMIN_IDS", None)
            else:
                os.environ["ADMIN_IDS"] = old_value

    def test_menu_list_embed_is_paginated_in_groups_of_twenty(self):
        menus = [f"메뉴 {index}" for index in range(1, 22)]

        first_page = Index.make_menu_list_embed(menus, page=0)
        second_page = Index.make_menu_list_embed(menus, page=1)

        self.assertEqual(len(first_page.fields), 20)
        self.assertEqual(len(second_page.fields), 1)
        self.assertTrue(all(field.inline for field in first_page.fields))
        self.assertEqual(first_page.fields[0].value, "메뉴 1")
        self.assertEqual(second_page.fields[0].value, "메뉴 21")
        self.assertIn("페이지 1 / 2", first_page.footer.text)# type: ignore


class QuizDbTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        Index.MENU_DB_FILE = Path(self.temp_dir.name) / "menus.db"
        Index.initialize_menu_db()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_level_cost_increases_at_level_tiers(self):
        self.assertEqual(Index.points_for_next_level(0), 20)
        self.assertEqual(Index.points_for_next_level(49), 1000)
        self.assertEqual(Index.points_for_next_level(50), 1050)
        self.assertEqual(Index.points_for_next_level(99), 3500)
        self.assertEqual(Index.points_for_next_level(100), 3600)
        self.assertEqual(Index.points_for_next_level(101), 3700)

    def test_quiz_cooldown_is_shared_and_expires_after_thirty_minutes(self):
        old_cooldown = Index.quiz_cooldown_until
        old_duration = Index.QUIZ_COOLDOWN_SECONDS
        try:
            Index.quiz_cooldown_until = None
            Index.QUIZ_COOLDOWN_SECONDS = 1800

            self.assertEqual(Index.claim_quiz_cooldown(now=1000), 0)
            self.assertEqual(Index.claim_quiz_cooldown(now=1100), 1700)
            self.assertEqual(Index.claim_quiz_cooldown(now=2800), 0)
        finally:
            Index.quiz_cooldown_until = old_cooldown
            Index.QUIZ_COOLDOWN_SECONDS = old_duration

    def test_level_embed_shows_level_and_remaining_points(self):
        embed = Index.make_level_embed("테스트", (2, 30, 60))

        self.assertEqual(embed.title, "테스트님의 레벨 정보")
        self.assertEqual(embed.fields[0].value, "Lv 2")
        self.assertEqual(embed.fields[1].value, "30 / 60p")
        self.assertEqual(embed.fields[2].value, "30p · 진행도 50%")

    def test_quiz_completion_embed_shows_solver_name(self):
        embed = Index.make_quiz_embed(
            "숫자 3을 한글로?",
            ["3", "삼", "셋"],
            1,
            0,
            40,
            revealed=True,
            completed=True,
            solver_name="테스트 사용자",
        )

        self.assertEqual(embed.title, "퀴즈 완료")
        self.assertIn("테스트 사용자", {field.value for field in embed.fields})

    def test_public_quiz_view_allows_another_user_to_participate(self):
        import asyncio

        view = Index.QuizView(
            1,
            202,
            1,
            "숫자 3을 한글로?",
            "하나 다음",
            ["3", "삼", "셋"],
            (0, 0, 20),
            public=True,
        )
        interaction = cast(
            Index.discord.Interaction,
            types.SimpleNamespace(user=types.SimpleNamespace(id=303)),
        )

        self.assertTrue(asyncio.run(view._check_user(interaction)))

    def test_quiz_abandonment_has_a_distinct_embed(self):
        embed = Index.make_quiz_abandoned_embed("숫자 3을 한글로?", ["3", "삼"], "테스트 사용자")

        self.assertEqual(embed.title, "퀴즈 포기")
        self.assertIsNotNone(embed.description)
        self.assertIn("테스트 사용자님이 퀴즈를 포기했습니다.", embed.description or "")
        self.assertEqual(embed.fields[0].name, "정답")

    def test_quiz_aliases_are_saved_and_reward_is_only_awarded_once(self):
        question_id = Index.add_quiz_question(
            1,
            "숫자 3을 한글로?",
            "하나 다음",
            ["3", "삼", "셋"],
            101,
        )

        self.assertEqual(
            Index.get_random_quiz(1, 202),
            (question_id, "숫자 3을 한글로?", "하나 다음", ["3", "삼", "셋"]),
        )
        self.assertEqual(Index.normalize_quiz_answer(" 세  셋 "), "세셋")
        self.assertEqual(Index.normalize_quiz_answer(" Some Answer "), "someanswer")

        with patch.object(Index, "QUIZ_REWARD_POINTS", 20):
            self.assertEqual(Index.award_quiz_points(1, question_id, 202), (True, 1, 0, 40))
            self.assertEqual(Index.award_quiz_points(1, question_id, 202), (False, 1, 0, 40))
            self.assertEqual(Index.award_quiz_points(1, question_id, 303), (True, 1, 0, 40))
            self.assertIsNone(Index.get_random_quiz(1, 202))
            self.assertIsNone(Index.get_random_quiz(1, 303))

    def test_reset_quiz_questions_only_clears_the_selected_guild(self):
        first_question = Index.add_quiz_question(1, "문제 1", "힌트", ["답"], 101)
        second_question = Index.add_quiz_question(2, "문제 2", "힌트", ["답"], 202)
        with patch.object(Index, "QUIZ_REWARD_POINTS", 20):
            Index.award_quiz_points(1, first_question, 303)

        self.assertEqual(Index.clear_quiz_questions(1), 1)
        self.assertIsNone(Index.get_random_quiz(1, 303))
        self.assertEqual(
            Index.get_random_quiz(2, 404),
            (second_question, "문제 2", "힌트", ["답"]),
        )
        self.assertEqual(Index.get_user_level(1, 303), (1, 0, 40))


class BotRegistrationTests(unittest.TestCase):
    def test_tig_command_is_registered(self):
        old_time = os.environ.pop("AUTO_MESSAGE_TIME", None)
        old_text = os.environ.pop("AUTO_MESSAGE_TEXT", None)
        try:
            bot = Index.ComicWorldBot(None)
            import asyncio
            asyncio.run(bot.setup_hook())
            self.assertIsNotNone(bot.get_command("티그"))
            self.assertIsNotNone(bot.tree.get_command("퀴즈"))
            self.assertIsNotNone(bot.tree.get_command("문제출제"))
            self.assertIsNotNone(bot.tree.get_command("내레벨"))
            self.assertIsNotNone(bot.tree.get_command("문제초기화"))
        finally:
            if old_time is not None:
                os.environ["AUTO_MESSAGE_TIME"] = old_time
            if old_text is not None:
                os.environ["AUTO_MESSAGE_TEXT"] = old_text


class CommandSyncTests(unittest.TestCase):
    def test_global_commands_are_synced_instead_of_cleared(self):
        import asyncio

        bot = Index.ComicWorldBot(None)
        with patch.object(bot.tree, "sync", new_callable=AsyncMock) as sync:
            asyncio.run(bot.sync_commands_with_retry())

        sync.assert_awaited_once_with()
        self.assertTrue(bot.commands_synced)


class InteractionLoggingTests(unittest.TestCase):
    def test_menu_list_attempt_is_logged_before_command_execution(self):
        import asyncio

        bot = Index.ComicWorldBot(None)
        interaction = types.SimpleNamespace(
            type=Index.discord.InteractionType.application_command,
            command=None,
            data={"name": "메뉴목록"},
            user=types.SimpleNamespace(id=1234),
        )

        with self.assertLogs(Index.logger.name, level="INFO") as captured:
            asyncio.run(bot.on_interaction(interaction))# type: ignore

        self.assertTrue(any("command:메뉴목록" in message for message in captured.output))
        self.assertTrue(any("user_id=1234" in message for message in captured.output))


class StatusHelpersTests(unittest.TestCase):
    def test_get_auto_message_time(self):
        old_value = os.environ.get("AUTO_MESSAGE_TIME")
        try:
            os.environ["AUTO_MESSAGE_TIME"] = "09:05"
            self.assertEqual(Index.get_auto_message_time(), (9, 5))
            os.environ["AUTO_MESSAGE_TIME"] = "25:00"
            self.assertIsNone(Index.get_auto_message_time())
        finally:
            if old_value is None:
                os.environ.pop("AUTO_MESSAGE_TIME", None)
            else:
                os.environ["AUTO_MESSAGE_TIME"] = old_value

    def test_get_auto_message_times_supports_multiple_times(self):
        old_value = os.environ.get("AUTO_MESSAGE_TIME")
        try:
            os.environ["AUTO_MESSAGE_TIME"] = "19:17, 19:18"
            self.assertEqual(Index.get_auto_message_times(), [(19, 17), (19, 18)])
        finally:
            if old_value is None:
                os.environ.pop("AUTO_MESSAGE_TIME", None)
            else:
                os.environ["AUTO_MESSAGE_TIME"] = old_value

    def test_get_auto_message_text_uses_time_specific_messages(self):
        old_value = os.environ.get("AUTO_MESSAGE_TEXTS")
        try:
            os.environ["AUTO_MESSAGE_TEXTS"] = '{"19:17":"첫 번째", "19:18":"두 번째"}'
            self.assertEqual(Index.get_auto_message_text((19, 17)), "첫 번째")
            self.assertEqual(Index.get_auto_message_text((19, 18)), "두 번째")
        finally:
            if old_value is None:
                os.environ.pop("AUTO_MESSAGE_TEXTS", None)
            else:
                os.environ["AUTO_MESSAGE_TEXTS"] = old_value

    def test_get_auto_message_channel_ids_uses_both_servers(self):
        old_value = os.environ.pop("AUTO_MESSAGE_CHANNEL_IDS", None)
        try:
            self.assertEqual(
                Index.get_auto_message_channel_ids(),
                [1549321583384862730],
            )
        finally:
            if old_value is not None:
                os.environ["AUTO_MESSAGE_CHANNEL_IDS"] = old_value

    def test_parse_ping_latency(self):
        raw = (
            "PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.\n"
            "64 bytes from 8.8.8.8: icmp_seq=1 ttl=118 time=13.2 ms\n"
        )
        self.assertEqual(Index.parse_ping_latency(raw), "13.2ms")

    def test_format_uptime_seconds(self):
        self.assertEqual(Index.format_uptime_seconds(90061), "1일 1시간 1분 1초")

    def test_parse_android_uptime_text(self):
        self.assertEqual(
            Index.parse_uptime_text("up 1 week, 22 hours, 12 minutes"),
            "7일 22시간 12분 0초",
        )


if __name__ == "__main__":
    unittest.main()
