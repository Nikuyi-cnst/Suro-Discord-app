import asyncio, hashlib, json, logging, math, os, random, re, shutil, sqlite3, subprocess, sys, threading, time, traceback, discord, requests, discord.ext
from datetime import date, datetime, timedelta, timezone
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

ClientBuild = "GA-Stable"
ClientVersion = "GA2.0-S"
ClientBuildDate = "KOO2609231000-20260926014607"

Help_Message_KOR = """# 슈로 봇 사용안내 (For Korean)
-# {mention}
# ✧ ----------≺ **메인** ≻---------- ✧
> 안녕하세요! 봇 개발자인 **<@924576483333259294>(Aren/아렌)**입니다.
> 이 문서는 해당 봇을 사용하는 방법을 알려드려요.
# ✧ ----------≺ **기능** ≻---------- ✧
> ### - `/코믹인포`
> `/코믹인포`는 **대한민국의 행사인 코믹월드의 정보**를 불러와줘요.
> _단, **10분마다 1번씩 **보낼 수 있어요._
> ### - `/코믹스케줄`
> `/코믹스케줄`은 **대한민국의 행사인 코믹월드의 정보를 원하는 많큼** 불러올 수 있어요.
> ### - `/메뉴추천`
> `/메뉴추천`은 **유저들이 등록한 식사 메뉴들을 불러올 수 있**어요.
> ### - `/메뉴등록`
> `/메뉴등록`은 **식사 메뉴를 등록**할 수 있어요. 
> ### - `/메뉴삭제`
> `/메뉴삭제`는 **본인이 등록한 메뉴를 삭제**할 수 있어요.
> ### - `/퀴즈`
> `/퀴즈`로 문제를 풀고 정답을 맞히면 레벨 포인트를 얻을 수 있어요.
> ### - `/문제출제`
> `/문제출제`로 문제, 힌트, 최대 4개의 정답을 입력해 바로 퀴즈를 출제할 수 있어요.
> ### - `/문의`
> `/문의`는 **피드백, 버그재보, 질문등의 모든것**을 받습니다.
> _명령어 전송시 개발자에게 즉시 DM이 전송됩니다._
> 버그재보가 아닌 이상 아무사진을 보내도 됩니다.
> __버그재보일경우, 해당 메시지를 캡처해서 보내주세요.__
> ### - `/상태`
> `/상태`는 말 그대로 봇의 상태를 볼 수 있어요.
> ### - `/도움말`
> `/도움말`은 이 문서를 볼 수 있어요.
# ✧ ----------≺ **기타 정보** ≻---------- ✧
> 추가 질문 사항이 있다면, `/문의`를 사용해보세요! 사진은 아무거나 보내도 됩니다.
> 다음 업데이트(GA1.4-S)에선 무엇이 추가될까요? 원하는 기능이 있다면, `/문의`를 통해서 말씀해보세요.
-# C-Build: {ClientBuild} / ClientVersion: {ClientVersion} / C-BuildDate: {ClientBuildDate}"""

Help_Message_JPN = """# 슈로「シュロ」ボット使用案内 (For Japanese)
-# {mention}
その文書は翻訳者を使用して書かれています。
誤解を招く可能性がある文があるかもしれません。参考にしてください！
# ✧ ----------≺ **メイン** ≻---------- ✧
> こんにちは！ボット開発者である**<@924576483333259294>(Aren/アレン)**です
> この記事では、そのボットの使い方を教えてくれます。
# ✧ ----------≺ **機能** ≻---------- ✧
> ### - `/코믹인포`
> `/코믹인포`(コミックインフォ)は**大韓民国のイベントであるコミックワールドの情報**を呼んでくれます。
> _ただし、**10分ごとに1回ずつ**送信できます。_
> ### - `/코믹스케줄`
> `/코믹스케줄`(コミックスケジュール)は **大韓民国のイベントであるコミックワールドの情報を欲しがる多く**呼べます。
> ### - `/메뉴추천`
> `/메뉴추천`(メニューおすすめ)は**ユーザーが登録した食事メニューを呼び出すことができます。**
> ### - `/메뉴등록`
> `/메뉴등록`(メニュー登録)は**食事メニューを登録**できます。
> ### - `/메뉴삭제`
> `/메뉴삭제`(メニュー削除)は**本人が登録したメニューを削除**できます。
> ### - `/퀴즈`
> `/퀴즈`(クイズ)で問題を解き、正解するとレベルポイントを獲得できます。
> ### - `/문제출제`
> `/문제출제`で問題、ヒント、最大4個の正解を入力し、その場で出題できます。
> ### - `/문의`
> `/문의`(お問い合わせ)は**フィードバック、バグ再報、質問などのすべてを受け取ります。
> _命令を送信すると、開発者にすぐにDMが送信されます。_
> バグジェボではない限り、何の写真も送れます。
> __エラーが発生した場合は、ボットが送信したメッセージをキャプチャして送信してください。__
> ### - `/상태`
> `/상태`(状態)は文字通りボットの状態を見ることができます。
> ### - `/도움말`
> `/도움말`(ヘルプ)はこの記事を見ることができます。
# ✧ ----------≺ **その他の情報** ≻---------- ✧
> さらに質問がある場合は、`/문의`（お問い合わせ）をお試しください！写真は何でも送信できます。
> 次のアップデート(GA1.4-S)では何が追加されますか？必要な機能がある場合は、`/문의`（お問い合わせ）を通して教えてください。
-# C-Build: {ClientBuild} / ClientVersion: {ClientVersion} / C-BuildDate: {ClientBuildDate}"""

Activity_Texts = {# 만우절 기간 전용으로 우로스 "낚시 하는중" 추가
	1: "아침공기 마시는중", #8:00 ~ 11:00
	3: "연회장에서 식사중", #11:00 ~ 13:00, 18:00 ~ 20:00
	4: "식사중", #11:00 ~ 13:00, 18:00 ~ 20:00
	5: "밥 씹는중", #0.5%의 확률 / 11:00 ~ 13:00, 18:00 ~ 20:00
	6: "티그랑 훈련중",#13:00 ~ 18:00
	7: "교주님을 따라 침략중",#13:00 ~ 18:00
	8: "추천할 메뉴 생각중",#13:00 ~ 18:00
	9: "산책 하는중",#13:00 ~ 18:00
	10: "밤 하늘 보는중", #18:00 ~ 20:00
	# 11: "낚시 하는중"# 만우절 시즌(4/1~4/7) 전용 / 13:00 ~ 18:00
}
ACTIVITY_PERIODS = {
	"morning": (1,),
	"late_morning": (3, 4, 5),
	"afternoon": (6, 7, 8, 9),
	"evening": (10, 9, 3),
}
BASE_URL = "https://comicw.net"
EVENTS_URL = f"{BASE_URL}/bbs/ajax.main.php"
COMICWORLD_EMOJI_URL = "https://cdn.discordapp.com/emojis/1549042252322439258.png"
CACHE_FILE = Path(__file__).with_name(".event_cache.json")
MENU_DB_FILE = Path(__file__).with_name("menus.db")
LOG_DIR = Path(__file__).with_name("logs")
LOG_FILE = LOG_DIR / "console.log"
MANUAL_LOG_DIR = LOG_DIR / "manual"
ERROR_LOG_DIR = LOG_DIR / "errors"
DEVELOPER_USER_ID = 924576483333259294
SCHEDULE_COOLDOWN_SECONDS = 600
QUIZ_COOLDOWN_SECONDS = 1800
TIG_COOLDOWN_SECONDS = 7200
TIG_EXECUTION_PROBABILITY = 0.0004
MENU_PAGE_SIZE = 20
QUIZ_REWARD_POINTS = random.randint(5, 20)
QUIZ_MAX_ANSWERS = 4
KST = timezone(timedelta(hours=9))
DEFAULT_AUTO_MESSAGE_CHANNEL_IDS = (
	1549321583384862730,
	# 1548640303337046138,
)
schedule_cooldown_until: float | None = None
quiz_cooldown_until: float | None = None
tig_cooldown_until: float | None = None
last_auto_message_dates: dict[int, date] = {}
activity_period: str | None = None
activity_change_count = 0
activity_current_text: str | None = None
activity_next_change_at: datetime | None = None

BOT_NAME = "Suro"
BOT_ON_MESSAGE = f"""
----------------------------------------------------                                                                           
Wellcome to {BOT_NAME} app log channel!

새 버전 출시! -  [KST]2026년 10월 01일 07시 00분
G2.0-S - 버전이 정식 출시되었스빈다.
자세한 내용은 '/도움말'을 참고하세요.

다음 업대이트는 GA2.1-S로 예정되어 있습니다.(아마도)
----------------------------------------------------
build: {ClientBuild}
version: {ClientVersion}
build date: {ClientBuildDate}
System Load Time: {time.ctime()}
------------------------------------------------"""

load_dotenv()

LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
	handlers=[
		logging.StreamHandler(sys.stdout),
		TimedRotatingFileHandler(
			LOG_FILE,
			when="midnight",
			interval=1,
			backupCount=30,
			encoding="utf-8",
		),
	],
)
logger = logging.getLogger("comicworld-loader")


def create_error_log(error: BaseException, context: str, traceback_text: str | None = None) -> Path:
	ERROR_LOG_DIR.mkdir(exist_ok=True)
	timestamp = datetime.now(KST)
	log_path = ERROR_LOG_DIR / f"error-{timestamp:%Y%m%d-%H%M%S-%f}.log"
	traceback_text = traceback_text or "".join(
		traceback.format_exception(type(error), error, error.__traceback__)
	)
	log_path.write_text(
		f"발생 시각: {timestamp.isoformat()}\n"
		f"오류 위치: {context}\n"
		f"오류 유형: {type(error).__name__}\n\n"
		f"{traceback_text}",
		encoding="utf-8",
	)
	return log_path


async def send_error_log_to_developer(
	bot: discord.Client,
	error: BaseException,
	context: str,
	traceback_text: str | None = None,
) -> None:
	try:
		log_path = create_error_log(error, context, traceback_text)
		developer = bot.get_user(DEVELOPER_USER_ID) or await bot.fetch_user(DEVELOPER_USER_ID)
		dm_channel = await developer.create_dm()
		await dm_channel.send(
			f"오류 로그가 자동 전송되었습니다.\n발생 위치: `{context}`",
			file=discord.File(str(log_path), filename=log_path.name),
		)
		logger.info("오류 로그를 개발자 DM으로 전송했습니다: %s", log_path)
	except Exception:
		logger.exception("오류 로그 생성 또는 개발자 DM 전송에 실패했습니다.")


def format_error_traceback(error: BaseException) -> str:
	return "".join(traceback.format_exception(type(error), error, error.__traceback__))


def save_log_snapshot() -> Path:
	for handler in logging.getLogger().handlers:
		handler.flush() 
	MANUAL_LOG_DIR.mkdir(exist_ok=True)
	snapshot_path = MANUAL_LOG_DIR / f"console-{datetime.now(KST):%Y%m%d-%H%M%S}.log"
	shutil.copyfile(LOG_FILE, snapshot_path)
	logger.info("로그를 수동 저장했습니다: %s", snapshot_path)
	return snapshot_path


def console_command_listener() -> None:
	while True:
		try:
			command = input().strip()
		except (EOFError, KeyboardInterrupt, OSError):
			return
		if command == "/로그저장":
			try:
				save_log_snapshot()
			except OSError:
				logger.exception("로그 수동 저장에 실패했습니다.")


def start_console_command_listener() -> None:
	threading.Thread(
		target=console_command_listener,
		name="console-command-listener",
		daemon=True,
	).start()


def required_env(name: str) -> str:
	value = os.getenv(name)
	if not value:
		raise RuntimeError(f"환경변수 {name}이(가) 설정되지 않았습니다.")
	return value


def get_auto_message_times() -> list[tuple[int, int]]:
	value = os.getenv("AUTO_MESSAGE_TIME", "").strip()
	if not value:
		return []

	times = []
	for item in value.split(","):
		try:
			hour, minute = (int(part) for part in item.strip().split(":", 1))
		except (TypeError, ValueError):
			logger.warning("AUTO_MESSAGE_TIME은 HH:MM 형식이어야 합니다: %s", item)
			continue
		if not (0 <= hour <= 23 and 0 <= minute <= 59):
			logger.warning("AUTO_MESSAGE_TIME이 올바른 시간이 아닙니다: %s", item)
			continue
		if (hour, minute) not in times:
			times.append((hour, minute))
	return times


def get_auto_message_time() -> tuple[int, int] | None:
	times = get_auto_message_times()
	return times[0] if times else None


def is_auto_message_day_allowed(current_time: tuple[int, int], weekday: int) -> bool:
	if current_time == (15, 0):
		return weekday == 0
	if current_time == (20, 0):
		return weekday == 3
	return True


def get_auto_message_text(current_time: tuple[int, int]) -> str | None:
	message_map = os.getenv("AUTO_MESSAGE_TEXTS", "").strip()
	if message_map:
		try:
			payload = json.loads(message_map)
		except json.JSONDecodeError:
			logger.warning("AUTO_MESSAGE_TEXTS는 JSON 형식이어야 합니다.")
			payload = {}
		if isinstance(payload, dict):
			key = f"{current_time[0]:02d}:{current_time[1]:02d}"
			message = payload.get(key)
			if isinstance(message, str) and message.strip():
				return message.strip()

	message = os.getenv("AUTO_MESSAGE_TEXT", "").strip()
	return message or None


def get_auto_message_channel_ids() -> list[int]:
	value = os.getenv("AUTO_MESSAGE_CHANNEL_IDS")
	if value is None:
		return list(DEFAULT_AUTO_MESSAGE_CHANNEL_IDS)

	channel_ids = []
	for item in value.split(","):
		candidate = item.strip()
		if not candidate:
			continue
		try:
			channel_id = int(candidate)
		except ValueError:
			logger.warning("AUTO_MESSAGE_CHANNEL_IDS에 잘못된 값이 포함되어 있습니다: %s", candidate)
			continue
		if channel_id > 0 and channel_id not in channel_ids:
			channel_ids.append(channel_id)
	return channel_ids


def fetch_events() -> list[dict[str, str]]:
	response = requests.post(
		EVENTS_URL,
		data={"type": "comic"},
		headers={"User-Agent": "ComicWorldDiscordBot/1.0"},
		timeout=15,
	)
	response.raise_for_status()
	data = response.json()
	if not isinstance(data, list):
		raise ValueError("코믹월드 행사 API가 예상과 다른 형식의 응답을 반환했습니다.")
	return data


def events_fingerprint(events: list[dict[str, str]]) -> str:
	payload = json.dumps(events, ensure_ascii=False, sort_keys=True)
	return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_cached_fingerprint() -> str | None:
	try:
		return json.loads(CACHE_FILE.read_text(encoding="utf-8")).get("fingerprint")
	except (FileNotFoundError, json.JSONDecodeError, AttributeError):
		return None


def save_cached_fingerprint(fingerprint: str) -> None:
	CACHE_FILE.write_text(
		json.dumps({"fingerprint": fingerprint}, ensure_ascii=False),
		encoding="utf-8",
	)


def initialize_menu_db() -> None:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS menus (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				guild_id INTEGER NOT NULL,
				owner_id INTEGER NOT NULL DEFAULT 0,
				menu TEXT NOT NULL,
				UNIQUE(guild_id, menu)
			)
			"""
		)
		connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS quiz_questions (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				guild_id INTEGER NOT NULL,
				question TEXT NOT NULL,
				hint TEXT NOT NULL,
				answers_json TEXT NOT NULL,
				created_by INTEGER NOT NULL
			)
			"""
		)
		connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS user_levels (
				guild_id INTEGER NOT NULL,
				user_id INTEGER NOT NULL,
				level INTEGER NOT NULL DEFAULT 0,
				points INTEGER NOT NULL DEFAULT 0,
				PRIMARY KEY (guild_id, user_id)
			)
			"""
		)
		connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS quiz_solves (
				guild_id INTEGER NOT NULL,
				question_id INTEGER NOT NULL,
				user_id INTEGER NOT NULL,
				PRIMARY KEY (guild_id, question_id, user_id)
			)
			"""
		)
		try:
			connection.execute("SELECT owner_id FROM menus LIMIT 1")
		except sqlite3.OperationalError:
			connection.execute(
				"ALTER TABLE menus ADD COLUMN owner_id INTEGER NOT NULL DEFAULT 0"
			)
		connection.commit()
	finally:
		connection.close()


def points_for_next_level(level: int) -> int:
	if level < 50:
		return (level + 1) * 20
	if level < 100:
		return 1000 + (level - 49) * 50
	return 3500 + (level - 99) * 100


def claim_quiz_cooldown(now: float | None = None) -> float:
	global quiz_cooldown_until
	current_time = time.monotonic() if now is None else now
	if quiz_cooldown_until is not None and quiz_cooldown_until > current_time:
		return quiz_cooldown_until - current_time
	quiz_cooldown_until = current_time + QUIZ_COOLDOWN_SECONDS
	return 0.0


def add_quiz_question(
	guild_id: int,
	question: str,
	hint: str,
	answers: list[str],
	created_by: int,
) -> int:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		cursor = connection.execute(
			"""
			INSERT INTO quiz_questions (guild_id, question, hint, answers_json, created_by)
			VALUES (?, ?, ?, ?, ?)
			""",
			(guild_id, question, hint, json.dumps(answers, ensure_ascii=False), created_by),
		)
		connection.commit()
		if cursor.lastrowid is None:
			raise RuntimeError("퀴즈 문제 ID를 가져오지 못했습니다.")
		return cursor.lastrowid
	finally:
		connection.close()


def clear_quiz_questions(guild_id: int) -> int:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		connection.execute("BEGIN IMMEDIATE")
		connection.execute("DELETE FROM quiz_solves WHERE guild_id = ?", (guild_id,))
		cursor = connection.execute(
			"DELETE FROM quiz_questions WHERE guild_id = ?",
			(guild_id,),
		)
		connection.commit()
		return cursor.rowcount
	finally:
		connection.close()


def get_random_quiz(guild_id: int, user_id: int) -> tuple[int, str, str, list[str]] | None:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		row = connection.execute(
			"""
			SELECT question.id, question.question, question.hint, question.answers_json
			FROM quiz_questions AS question
			WHERE question.guild_id = ?
			AND NOT EXISTS (
				SELECT 1 FROM quiz_solves AS solve
				WHERE solve.guild_id = question.guild_id
				AND solve.question_id = question.id
				AND solve.user_id = ?
			)
			ORDER BY RANDOM()
			LIMIT 1
			""",
			(guild_id, user_id),
		).fetchone()
		if row is None:
			return None
		question_id, question, hint, answers_json = row
		return question_id, question, hint, json.loads(answers_json)
	finally:
		connection.close()


def get_user_level(guild_id: int, user_id: int) -> tuple[int, int, int]:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		row = connection.execute(
			"SELECT level, points FROM user_levels WHERE guild_id = ? AND user_id = ?",
			(guild_id, user_id),
		).fetchone()
		level, points = row if row is not None else (0, 0)
		return level, points, points_for_next_level(level)
	finally:
		connection.close()


def award_quiz_points(
	guild_id: int,
	question_id: int,
	user_id: int,
) -> tuple[bool, int, int, int]:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		connection.execute("BEGIN IMMEDIATE")
		connection.execute(
			"INSERT OR IGNORE INTO user_levels (guild_id, user_id) VALUES (?, ?)",
			(guild_id, user_id),
		)
		cursor = connection.execute(
			"INSERT OR IGNORE INTO quiz_solves (guild_id, question_id, user_id) VALUES (?, ?, ?)",
			(guild_id, question_id, user_id),
		)
		if cursor.rowcount == 0:
			row = connection.execute(
				"SELECT level, points FROM user_levels WHERE guild_id = ? AND user_id = ?",
				(guild_id, user_id),
			).fetchone()
			level, points = row
			connection.commit()
			return False, level, points, points_for_next_level(level)

		row = connection.execute(
			"SELECT level, points FROM user_levels WHERE guild_id = ? AND user_id = ?",
			(guild_id, user_id),
		).fetchone()
		level, points = row
		points += QUIZ_REWARD_POINTS
		while points >= points_for_next_level(level):
			level += 1
			points = 0
		connection.execute(
			"UPDATE user_levels SET level = ?, points = ? WHERE guild_id = ? AND user_id = ?",
			(level, points, guild_id, user_id),
		)
		connection.commit()
		return True, level, points, points_for_next_level(level)
	finally:
		connection.close()


def make_quiz_embed(
	question: str,
	answers: list[str],
	level: int,
	points: int,
	required_points: int,
	revealed: bool = False,
	completed: bool = False,
	show_progress: bool = True,
	solver_name: str | None = None,
) -> discord.Embed:
	embed = discord.Embed(
		title="퀴즈 완료" if completed else "퀴즈",
		description=question,
		color=discord.Color.green() if completed else discord.Color.blurple(),
	)
	if revealed:
		embed.add_field(name="정답", value=" / ".join(answers), inline=False)
	if solver_name:
		embed.add_field(name="정답자", value=solver_name, inline=False)
	footer = (
		f"정답 보상 {QUIZ_REWARD_POINTS}p"
		if show_progress  
		else f"정답 보상 {QUIZ_REWARD_POINTS}p"
	)
	embed.set_footer(text=footer)
	return embed


def make_quiz_abandoned_embed(question: str, answers: list[str], user_name: str) -> discord.Embed:
	embed = discord.Embed(
		title="퀴즈 포기",
		description=f"{user_name}님이 퀴즈를 포기했습니다.\n\n{question}",
		color=discord.Color.orange(),
	)
	embed.add_field(name="정답", value=" / ".join(answers), inline=False)
	return embed


def make_level_embed(user_name: str, progress: tuple[int, int, int]) -> discord.Embed:
	level, points, required_points = progress
	remaining_points = required_points - points
	progress_percent = int(points / required_points * 100)
	embed = discord.Embed(
		title=f"{user_name}님의 레벨 정보",
		color=discord.Color.green(),
	)
	embed.add_field(name="레벨", value=f"Lv {level}", inline=True)
	embed.add_field(
		name="현재 포인트",
		value=f"{points} / {required_points}p",
		inline=True,
	)
	embed.add_field(
		name="다음 레벨까지",
		value=f"{remaining_points}p · 진행도 {progress_percent}%",
		inline=False,
	)
	return embed


def normalize_quiz_answer(answer: str) -> str:
	return re.sub(r"\s+", "", answer).casefold()


class QuizView(discord.ui.View):
	def __init__(
		self,
		guild_id: int,
		user_id: int,
		question_id: int,
		question: str,
		hint: str,
		answers: list[str],
		progress: tuple[int, int, int],
		public: bool = False,
	) -> None:
		super().__init__(timeout=180)
		self.guild_id = guild_id
		self.user_id = user_id
		self.question_id = question_id
		self.question = question
		self.hint = hint
		self.answers = answers
		self.level, self.points, self.required_points = progress
		self.public = public
		self.message: discord.InteractionMessage | None = None
		self.finished = False
		self.solved_users: set[int] = set()
		self.completion_lock = asyncio.Lock()

	async def _check_user(self, interaction: discord.Interaction) -> bool:
		if self.public or interaction.user.id == self.user_id:
			return True
		await interaction.response.send_message(
			"이 퀴즈를 시작한 사용자만 사용할 수 있습니다.",
			ephemeral=True,
		)
		return False

	@discord.ui.button(label="힌트", style=discord.ButtonStyle.secondary)
	async def hint_button(
		self,
		interaction: discord.Interaction,
		button: discord.ui.Button,
	) -> None:
		if not await self._check_user(interaction):
			return
		if self.finished:
			await interaction.response.send_message("이미 종료된 퀴즈입니다.", ephemeral=True)
			return
		await interaction.response.send_message(f"힌트: {self.hint}", ephemeral=True)

	@discord.ui.button(label="정답 입력", style=discord.ButtonStyle.primary)
	async def answer_button(
		self,
		interaction: discord.Interaction,
		button: discord.ui.Button,
	) -> None:
		if not await self._check_user(interaction):
			return
		if self.finished:
			await interaction.response.send_message("이미 종료된 퀴즈입니다.", ephemeral=True)
			return
		await interaction.response.send_modal(QuizAnswerModal(self))

	@discord.ui.button(label="포기", style=discord.ButtonStyle.danger)
	async def give_up_button(
		self,
		interaction: discord.Interaction,
		button: discord.ui.Button,
	) -> None:
		if not await self._check_user(interaction):
			return
		if self.public and interaction.user.id != self.user_id:
			await interaction.response.send_message(
				"문제를 출제한 사용자만 퀴즈를 종료할 수 있습니다.",
				ephemeral=True,
			)
			return
		if self.finished:
			await interaction.response.send_message("이미 종료된 퀴즈입니다.", ephemeral=True)
			return
		self.finished = True
		await interaction.response.edit_message(
			embed=make_quiz_abandoned_embed(
				self.question,
				self.answers,
				interaction.user.display_name,
			),
			view=None,
		)


class QuizAnswerModal(discord.ui.Modal, title="정답 입력"):
	def __init__(self, quiz_view: QuizView) -> None:
		super().__init__()
		self.quiz_view = quiz_view
		self.answer = discord.ui.TextInput(
			label="정답",
			placeholder="정답을 입력하세요",
			max_length=200,
		)
		self.add_item(self.answer)

	async def on_submit(self, interaction: discord.Interaction) -> None:
		view = self.quiz_view
		if not await view._check_user(interaction):
			return
		if view.finished:
			await interaction.response.send_message("이미 종료된 퀴즈입니다.", ephemeral=True)
			return

		if normalize_quiz_answer(self.answer.value) not in {
			normalize_quiz_answer(answer) for answer in view.answers
		}:
			await interaction.response.send_message("틀렸어요. 다시 생각해보세요!", ephemeral=True)
			return

		await interaction.response.defer(ephemeral=True)
		async with view.completion_lock:
			if view.finished:
				await interaction.followup.send("이 퀴즈는 이미 완료되었습니다.", ephemeral=True)
				return
			if interaction.user.id in view.solved_users:
				await interaction.followup.send("이미 이 퀴즈의 정답을 맞혔습니다.", ephemeral=True)
				return

			awarded, level, points, required = await asyncio.to_thread(
				award_quiz_points,
				view.guild_id,
				view.question_id,
				interaction.user.id,
			)
			view.finished = True
			view.solved_users.add(interaction.user.id)
			view.level, view.points, view.required_points = level, points, required
			if view.message is not None:
				await view.message.edit(
					embed=make_quiz_embed(
						view.question,
						view.answers,
						level,
						points,
						required,
						revealed=True,
						completed=True,
						solver_name=interaction.user.display_name,
					),
					view=None,
				)
			if awarded:
				result = f"정답입니다! **{QUIZ_REWARD_POINTS}p**를 얻었습니다. 현재 **Lv {level} · {points}/{required}p**입니다."
			else:
				result = "정답입니다! 이미 푼 문제라 포인트는 다시 지급되지 않습니다."
			await interaction.followup.send(result, ephemeral=True)


def add_menu(guild_id: int, menu: str, owner_id: int) -> bool:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		cursor = connection.execute(
			"INSERT OR IGNORE INTO menus (guild_id, menu, owner_id) VALUES (?, ?, ?)",
			(guild_id, menu, owner_id),
		)
		connection.commit()
		return cursor.rowcount == 1
	finally:
		connection.close()


def get_menu_entries(guild_id: int) -> list[str]:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		menus = connection.execute(
			"SELECT menu FROM menus WHERE guild_id = ? ORDER BY menu COLLATE NOCASE",
			(guild_id,),
		).fetchall()
		return [menu for (menu,) in menus]
	finally:
		connection.close()


def make_menu_list_embed(menus: list[str], page: int = 0) -> discord.Embed:
	page_count = max(1, math.ceil(len(menus) / MENU_PAGE_SIZE))
	page = min(max(page, 0), page_count - 1)
	start = page * MENU_PAGE_SIZE
	embed = discord.Embed(
		title="등록된 메뉴 목록",
		color=discord.Color.green(),
	)
	for index, menu in enumerate(menus[start : start + MENU_PAGE_SIZE], start=start + 1):
		embed.add_field(name=f"{index}.", value=menu, inline=True)
	embed.set_footer(text=f"페이지 {page + 1} / {page_count} · 전체 {len(menus)}개")
	return embed


def delete_menu(guild_id: int, menu: str, user_id: int, is_admin: bool = False) -> bool:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		if is_admin:
			cursor = connection.execute(
				"DELETE FROM menus WHERE guild_id = ? AND menu = ?",
				(guild_id, menu),
			)
		else:
			cursor = connection.execute(
				"DELETE FROM menus WHERE guild_id = ? AND menu = ? AND owner_id = ?",
				(guild_id, menu, user_id),
			)
		connection.commit()
		return cursor.rowcount == 1
	finally:
		connection.close()


class MenuListView(discord.ui.View):
	def __init__(self, menus: list[str], requester_id: int) -> None:
		super().__init__(timeout=120)
		self.menus = menus
		self.requester_id = requester_id
		self.page = 0
		self.page_count = max(1, math.ceil(len(menus) / MENU_PAGE_SIZE))
		self._update_buttons()

	def _update_buttons(self) -> None:
		self.previous_button.disabled = self.page == 0
		self.next_button.disabled = self.page >= self.page_count - 1

	async def _change_page(self, interaction: discord.Interaction, page: int) -> None:
		if interaction.user.id != self.requester_id:
			await interaction.response.send_message(
				"이 메뉴 목록을 실행한 사용자만 페이지를 넘길 수 있습니다.",
				ephemeral=True,
			)
			return

		self.page = page
		self._update_buttons()
		await interaction.response.edit_message(
			embed=make_menu_list_embed(self.menus, self.page),
			view=self,
		)

	@discord.ui.button(label="이전", style=discord.ButtonStyle.secondary)
	async def previous_button(
		self,
		interaction: discord.Interaction,
		button: discord.ui.Button,
	) -> None:
		await self._change_page(interaction, self.page - 1)

	@discord.ui.button(label="다음", style=discord.ButtonStyle.primary)
	async def next_button(
		self,
		interaction: discord.Interaction,
		button: discord.ui.Button,
	) -> None:
		await self._change_page(interaction, self.page + 1)


def clear_menus(guild_id: int) -> int:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		cursor = connection.execute(
			"DELETE FROM menus WHERE guild_id = ?",
			(guild_id,),
		)
		connection.commit()
		return cursor.rowcount
	finally:
		connection.close()


def get_random_menu(guild_id: int) -> tuple[str | None, int]:
	connection = sqlite3.connect(MENU_DB_FILE)
	try:
		menus = connection.execute(
			"SELECT menu FROM menus WHERE guild_id = ?",
			(guild_id,),
		).fetchall()
		return (random.choice(menus)[0], len(menus)) if menus else (None, 0)
	finally:
		connection.close()


def format_menu_recommendation(menu: str) -> str:
	if random.random() < 0.001:
		return "# _난 마들렌이야_"

	return random.choice(
		[
			f"오늘의 추천 메뉴, **{menu}**을(를) 먹어보세요!",
			f"오늘 메뉴는 고민할 것도 없이 **{menu}**을(를) 먹어봐요.",
			f"오늘의 메뉴는 **{menu}**인거사와요.",
		]
	)


def get_admin_ids() -> set[int]:
	value = os.getenv("ADMIN_IDS") or os.getenv("MENU_ADMIN_IDS", "")
	admins: set[int] = set()
	for item in value.split(","):
		candidate = item.strip()
		if not candidate:
			continue
		try:
			admins.add(int(candidate))
		except ValueError:
			logger.warning("ADMIN_IDS에 잘못된 값이 포함되어 있습니다: %s", candidate)
	return admins


def get_admin_channel_id() -> int | None:
	channel_id = os.getenv("ADMIN_CHANNEL_ID")
	if not channel_id:
		return None
	try:
		return int(channel_id)
	except ValueError:
		logger.warning("ADMIN_CHANNEL_ID가 올바른 숫자가 아닙니다: %s", channel_id)
		return None


def parse_ping_latency(raw_output: str) -> str:
	match = re.search(r"time=(\d+(?:\.\d+)?)\s*ms", raw_output, re.IGNORECASE)
	if match:
		return f"{match.group(1)}ms"
		
	match = re.search(r"round-trip min/avg/max/stddev = .*?/((?:\d+(?:\.\d+)?)) ms", raw_output, re.IGNORECASE)
	if match:
		return f"{match.group(1)}ms"
	
	match = re.search(r"\b(\d+(?:\.\d+)?)\s*ms\b", raw_output, re.IGNORECASE)
	if match:
		return f"{match.group(1)}ms"
	
	return "측정 실패"


def format_uptime_seconds(total_seconds: float | int) -> str:
	total = int(total_seconds)
	days, remainder = divmod(total, 86400)
	hours, remainder = divmod(remainder, 3600)
	minutes, seconds = divmod(remainder, 60)
	parts = []
	if days:
		parts.append(f"{days}일")
	if hours or days:
		parts.append(f"{hours}시간")
	if minutes or hours or days:
		parts.append(f"{minutes}분")
	parts.append(f"{seconds}초")
	return " ".join(parts)


def parse_uptime_text(uptime_text: str) -> str:
	units = {
		"week": 604800,
		"weeks": 604800,
		"day": 86400,
		"days": 86400,
		"hour": 3600,
		"hours": 3600,
		"minute": 60,
		"minutes": 60,
		"second": 1,
		"seconds": 1,
	}
	total_seconds = 0
	for value, unit in re.findall(r"(\d+)\s+(weeks?|days?|hours?|minutes?|seconds?)", uptime_text.lower()):
		total_seconds += int(value) * units[unit]
	return format_uptime_seconds(total_seconds) if total_seconds else "-"


def read_text_file(path: str) -> str:
	try:
		return Path(path).read_text(encoding="utf-8", errors="replace")
	except OSError:
		return ""


def get_android_device_model() -> str:
	for cmd in (["getprop", "ro.product.model"], ["cat", "/system/build.prop"]):
		try:
			result = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=2)
		except (FileNotFoundError, subprocess.TimeoutExpired):
			continue
		if result.returncode == 0:
			output = result.stdout.strip()
			if not output:
				continue
			for line in output.splitlines():
				if "ro.product.model" in line:
					value = line.split("=", 1)[1].strip()
					if value:
						return value
			if output and "model" not in output.lower():
				return output.splitlines()[0].strip()
	return "SM-F731N"


def get_ram_usage() -> tuple[str, str, str]:
	meminfo = read_text_file("/proc/meminfo")
	if meminfo:
		values: dict[str, int] = {}
		for line in meminfo.splitlines():
			if not line.strip():
				continue
			key, value = line.split(":", 1)
			if key.strip() in {"MemTotal", "MemAvailable", "MemFree"}:
				try:
					values[key.strip()] = int(value.strip().split()[0])
				except (IndexError, ValueError):
					continue
		if "MemTotal" in values and "MemAvailable" in values:
			total_kb = values["MemTotal"]
			available_kb = values["MemAvailable"]
			used_kb = max(0, total_kb - available_kb)
			percent = 0 if total_kb == 0 else round((used_kb / total_kb) * 100)
			return f"{used_kb / 1024:.0f}MB", f"{total_kb / 1024:.0f}MB", f"{percent}%"

	for cmd in (["free", "-m"], ["free", "-k"]):
		try:
			result = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=3)
		except (FileNotFoundError, subprocess.TimeoutExpired):
			continue
		if result.returncode != 0:
			continue
		lines = result.stdout.splitlines()
		if len(lines) < 2:
			continue
		parts = lines[1].split()
		if len(parts) < 3:
			continue
		total = int(parts[1])
		used = int(parts[2])
		percent = 0 if total == 0 else round((used / total) * 100)
		if cmd[1] == "-m":
			return f"{used:.0f}MB", f"{total:.0f}MB", f"{percent}%"
		return f"{used / 1024:.0f}MB", f"{total / 1024:.0f}MB", f"{percent}%"

	return "-", "-", "-"


def get_cpu_usage() -> str:
	try:
		stat_before = read_text_file("/proc/stat").splitlines()[0]
		before_fields = stat_before.split()[1:]
		before_total = sum(int(value) for value in before_fields)
		before_idle = int(before_fields[3])
		time.sleep(1.0)
		stat_after = read_text_file("/proc/stat").splitlines()[0]
		after_fields = stat_after.split()[1:]
		after_total = sum(int(value) for value in after_fields)
		after_idle = int(after_fields[3])
		delta_total = after_total - before_total
		delta_idle = after_idle - before_idle
		if delta_total <= 0:
			return "-"
		usage = max(0.0, 100.0 * (1.0 - (delta_idle / delta_total)))
		return f"{usage:.1f}%"
	except (IndexError, ValueError, OSError):
		try:
			loadavg = read_text_file("/proc/loadavg").split()
			if loadavg:
				cpu_count = os.cpu_count() or 1
				return f"{min(100.0, max(0.0, float(loadavg[0]) / cpu_count * 100)):.1f}%"
			get_loadavg = getattr(os, "getloadavg", None)
			if get_loadavg is None:
				return "-"
			load_1m = get_loadavg()[0]
			cpu_count = os.cpu_count() or 1
			return f"{min(100.0, max(0.0, load_1m / cpu_count * 100)):.1f}%"
		except (AttributeError, OSError):
			pass
	try:
		result = subprocess.run(
			["top", "-b", "-n", "1"],
			capture_output=True,
			text=True,
			check=False,
			timeout=3,
		)
		cpu_match = re.search(r"(?:Cpu\(s\)|CPU):\s*(?:[\d.]+\s*us,\s*)?([\d.]+)\s*id", result.stdout, re.IGNORECASE)
		if result.returncode == 0 and cpu_match:
			return f"{max(0.0, 100.0 - float(cpu_match.group(1))):.1f}%"
		cpu_match = re.search(r"(?:CPU usage|CPU):\s*([\d.]+)%\s*(?:user|us).*?([\d.]+)%\s*idle", result.stdout, re.IGNORECASE)
		if result.returncode == 0 and cpu_match:
			return f"{max(0.0, 100.0 - float(cpu_match.group(2))):.1f}%"
	except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
		pass
	for command in (["dumpsys", "cpuinfo"], ["/system/bin/dumpsys", "cpuinfo"]):
		try:
			result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=3)
		except (FileNotFoundError, subprocess.TimeoutExpired):
			continue
		if result.returncode != 0:
			continue
		cpu_match = re.search(r"Total CPU usage:\s*([\d.]+)%", result.stdout, re.IGNORECASE)
		if cpu_match:
			return f"{float(cpu_match.group(1)):.1f}%"
	logger.warning("CPU 사용량을 계산하지 못했습니다. /proc/stat 또는 top 출력을 확인하세요.")
	return "-"


def get_ping_latency() -> str:
	for command in (["ping", "-c", "1", "-W", "2", "8.8.8.8"], ["ping", "-c", "1", "1.1.1.1"], ["ping", "-c", "1", "localhost"]):
		try:
			result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=3)
		except (FileNotFoundError, subprocess.TimeoutExpired):
			continue
		output = (result.stdout or "") + (result.stderr or "")
		if not output:
			continue
		parsed = parse_ping_latency(output)
		if parsed != "측정 실패":
			return parsed
	return "측정 실패"


def get_uptime() -> str:
	uptime_text = read_text_file("/proc/uptime")
	if uptime_text:
		try:
			return format_uptime_seconds(float(uptime_text.split()[0]))
		except (IndexError, ValueError):
			pass
	try:
		result = subprocess.run(["uptime", "-p"], capture_output=True, text=True, check=False, timeout=2)
		if result.returncode == 0 and result.stdout.strip():
			parsed = parse_uptime_text(result.stdout)
			if parsed != "-":
				return parsed
	except (FileNotFoundError, subprocess.TimeoutExpired):
		pass
	try:
		clock_boottime = getattr(time, "CLOCK_BOOTTIME", None)
		get_clock_time = getattr(time, "clock_gettime", None)
		if clock_boottime is not None and get_clock_time is not None:
			return format_uptime_seconds(get_clock_time(clock_boottime))
	except (AttributeError, OSError):
		pass
	return "-"


def get_storage_usage() -> tuple[str, str, str]:
	for path in ["/data", "/", "/storage/emulated/0"]:
		try:
			usage = shutil.disk_usage(path)
			total_bytes = usage.total
			used_bytes = usage.used
			percent = 0 if total_bytes == 0 else round((used_bytes / total_bytes) * 100)
			return f"{used_bytes / (1024 ** 3):.1f}GB", f"{total_bytes / (1024 ** 3):.1f}GB", f"{percent}%"
		except OSError:
			pass

		try:
			result = subprocess.run(["df", "-k", path], capture_output=True, text=True, check=False, timeout=2)
		except (FileNotFoundError, subprocess.TimeoutExpired):
			continue
		if result.returncode != 0:
			continue
		lines = result.stdout.strip().splitlines()
		if len(lines) < 2:
			continue
		columns = lines[1].split()
		if len(columns) < 4:
			continue
		try:
			total_kb = int(columns[1])
			used_kb = int(columns[2])
		except ValueError:
			continue
		percent = 0 if total_kb == 0 else round((used_kb / total_kb) * 100)
		return f"{used_kb / 1024:.1f}GB", f"{total_kb / 1024:.1f}GB", f"{percent}%"
	return "-", "-", "-"


def get_system_status_snapshot(uptime_override: str | None = None) -> dict[str, str]:
	device_model = get_android_device_model()
	ram_used, ram_total, ram_percent = get_ram_usage()
	ping_latency = get_ping_latency()
	uptime = uptime_override or get_uptime()
	storage_used, storage_total, storage_percent = get_storage_usage()
	return {
		"device_model": device_model,
		"ram_used": ram_used,
		"ram_total": ram_total,
		"ram_percent": ram_percent,
		"ping": ping_latency,
		"uptime": uptime,
		"storage_used": storage_used,
		"storage_total": storage_total,
		"storage_percent": storage_percent,
	}


def is_menu_admin(user: discord.abc.User | discord.User | discord.Member | None) -> bool:
	if user is None:
		return False
	if isinstance(user, discord.Member) and user.guild_permissions.administrator:
		return True
	return user.id in get_admin_ids()


def get_activity_period(current_time: datetime) -> str | None:
	hour = current_time.hour
	if 8 <= hour < 11:
		return "morning"
	if 11 <= hour < 13:
		return "late_morning"
	if 13 <= hour < 18:
		return "afternoon"
	if 18 <= hour < 20:
		return "evening"
	return None


def get_activity_change_delay_hours() -> float:
	return random.uniform(1, 4)


def choose_activity_text(period: str, previous_text: str | None = None) -> str:
	activity_ids = ACTIVITY_PERIODS[period]
	if period == "late_morning" and random.random() < 0.005:
		candidates = [Activity_Texts[5]]
	else:
		candidates = [Activity_Texts[activity_id] for activity_id in activity_ids if Activity_Texts[activity_id] != previous_text]
	if not candidates:
		candidates = [Activity_Texts[activity_id] for activity_id in activity_ids]
	return random.choice(candidates)


class HelpLanguageSelect(discord.ui.Select):
	def __init__(self, requester_id: int) -> None:
		super().__init__(
			placeholder="도움말 언어를 선택하세요 / 言語を選択してください",
			options=[
				discord.SelectOption(label="한국어", value="kor", description="한국어 도움말"),
				discord.SelectOption(label="日本語", value="jpn", description="日本語のヘルプ"),
			],
		)
		self.requester_id = requester_id

	async def callback(self, interaction: discord.Interaction) -> None:
		if interaction.user.id != self.requester_id:
			await interaction.response.send_message(
				"이 도움말 선택 메뉴를 실행한 사용자만 사용할 수 있습니다.",
				ephemeral=True,
			)
			return

		help_message = Help_Message_KOR if self.values[0] == "kor" else Help_Message_JPN
		help_message = help_message.format(
			mention=interaction.user.mention,
			ClientBuild=ClientBuild,
			ClientVersion=ClientVersion,
			ClientBuildDate=ClientBuildDate,
		)
		try:
			await interaction.user.send(help_message)
		except discord.Forbidden:
			await interaction.response.send_message(
				"DM을 보낼 수 없습니다. 사용자 설정에서 서버 멤버의 DM 수신을 허용해주세요.",
				ephemeral=True,
			)
			return
		except discord.HTTPException as error:
			logger.exception("도움말 DM 전송 실패: user_id=%s", interaction.user.id)
			await send_error_log_to_developer(interaction.client, error, "도움말 DM 전송")
			await interaction.response.send_message(
				"도움말을 DM으로 보내지 못했습니다. 잠시 후 다시 시도해주세요.",
				ephemeral=True,
			)
			return

		view = self.view
		if view is not None:
			view.stop()
			for child in view.children:
				child.disabled = True
		await interaction.response.edit_message(
			content="도움말을 DM으로 보냈습니다.",
			view=view,
		)


class HelpLanguageView(discord.ui.View):
	def __init__(self, requester_id: int) -> None:
		super().__init__(timeout=120)
		self.add_item(HelpLanguageSelect(requester_id))


@app_commands.command(
	name="도움말",
	description="도움말 언어를 선택해 DM으로 받습니다.",
)
async def help_command(interaction: discord.Interaction) -> None:
	await interaction.response.send_message(
		"도움말을 받을 언어를 선택해주세요.",
		view=HelpLanguageView(interaction.user.id),
		ephemeral=True,
		
	)


@commands.command(name="버터")
async def butter_command(ctx: commands.Context) -> None:
	logger.info(
			"CommandTriggered: , command:{command.name}, user_id=%s, username=%s",
			ctx.author.id,
			str(ctx.author),
	
		)
	message = (
		"각그랜저다!!!"
		if ctx.author.id in get_admin_ids()
		else "안녕하세요 저는 버터애요!"
	)
	await ctx.send(message)

@commands.command(name="티그")
async def tig_command(ctx: commands.Context) -> None:
	global tig_cooldown_until
	now = time.monotonic()
	if random.random() >= TIG_EXECUTION_PROBABILITY:
		return
	if tig_cooldown_until is not None:
		remaining = tig_cooldown_until - now
		if remaining > 0:
			remaining_minutes = math.ceil(remaining / 60)
			try:
				await ctx.message.delete()
			except discord.HTTPException:
				logger.debug("티그 쿨타임 안내를 위해 호출 메시지를 삭제하지 못했습니다.")
			try:
				await ctx.author.send(
					f"이 명령어는 전체 2시간 쿨타임이 있습니다. {remaining_minutes}분 후 다시 시도해주세요."
				)
			except discord.Forbidden:
				logger.warning("티그 쿨타임 안내 DM이 차단되었습니다: user_id=%s", ctx.author.id)
			return
	tig_cooldown_until = now + TIG_COOLDOWN_SECONDS
	logger.info(
			"CommandTriggered: , command:{command.name}, user_id=%s, username=%s",
			ctx.author.id,
			str(ctx.author),
	
		)
	message = random.choice(
		[
			"허~졉♡ 이딴게 좋은거야~? 최악♡최저♡ 저질이네♡ 역겨워...♡",
			"허졉 이딴말을 듣고싶어서 그런 글이나 싸지르고 정말한심하네♡",
			"허접~ 주제를 알아야지♡ 역겨우니까 말 걸지 마♡",
			"시끄러워♡ 허접 주제에 울기나 하고...♡",
			"허접... 이예요오...",
		]
	)
	try:
		await ctx.message.delete()
	except discord.HTTPException:
		logger.debug("티그 응답을 비공개로 보내기 위해 호출 메시지를 삭제하지 못했습니다.")
	try:
		await ctx.author.send(message)
	except discord.Forbidden:
		logger.warning("티그 응답 DM이 차단되었습니다: user_id=%s", ctx.author.id)
	


@commands.command(name="cnstSuro:stop")
async def stop_command(ctx: commands.Context) -> None:
	if ctx.author.id not in get_admin_ids():
		logger.info(
				"CommandTriggered: , command:{command.name}, user_id=%s, username=%s",
				ctx.author.id,
				str(ctx.author),
		
			)
		await ctx.send("# _난 마들렌이야_")
		return
	await ctx.bot.close()


@app_commands.command(
	name="상태",
	description="Termux 기반 Android 서버 상태를 확인합니다.",
)
async def status_command(interaction: discord.Interaction) -> None:
	interaction_age = max(0.0, time.time() - interaction.created_at.timestamp())
	logger.info(
		"상태 명령어 수신: interaction_id=%s, age=%.3fs, latency=%sms",
		interaction.id,
		interaction_age,
		getattr(interaction.client.ws, "latency", 0) * 1000,
	)
	try:
		await interaction.response.send_message("서버 상태를 조회하고 있습니다...", ephemeral=True)
	except discord.NotFound:
		logger.warning(
			"상태 명령어의 초기 응답이 만료되었습니다: interaction_id=%s, age=%.3fs",
			interaction.id,
			interaction_age,
		)
		return
	except discord.HTTPException as error:
		logger.exception("상태 명령어 초기 응답 실패: status=%s", error.status)
		return

	try:
		login_started_at = getattr(interaction.client, "login_started_at", None)
		uptime_override = (
			format_uptime_seconds(time.monotonic() - login_started_at)
			if login_started_at is not None
			else None
		)
		status = await asyncio.wait_for(
			asyncio.to_thread(get_system_status_snapshot, uptime_override),
			timeout=12,
		)
	except Exception as error:
		logger.exception("상태 조회 실패: %s", error)
		try:
			await interaction.edit_original_response(
				content="서버 상태를 불러오지 못했습니다. Termux 환경이 정상인지 확인해주세요."
			)
		except discord.NotFound:
			logger.warning("상태 명령어 오류 안내가 만료되었습니다: interaction_id=%s", interaction.id)
		return

	embed = discord.Embed(
		title=f"{status['device_model']} 서버 상태",
		color=discord.Color.green(),
	)
	embed.add_field(
		name="RAM 사용량",
		value=f"{status['ram_used']} / {status['ram_total']} ({status['ram_percent']})",
		inline=True,
	)
	embed.add_field(
		name="통신속도(핑)",
		value=status['ping'],
		inline=True,
	)
	embed.add_field(
		name="가동시간",
		value=status['uptime'],
		inline=True,
	)
	embed.add_field(
		name="스토리지",
		value=f"{status['storage_used']} / {status['storage_total']} ({status['storage_percent']})",
		inline=True,
	)
	embed.set_footer(text="Powered by Nikuyi")
	try:
		await interaction.edit_original_response(content=None, embed=embed)
	except discord.NotFound:
		logger.warning("상태 명령어 결과 전송이 만료되었습니다: interaction_id=%s", interaction.id)



@app_commands.command(
	name="로그저장",
	description="현재까지의 로그를 저장합니다. 관리자 전용.",
)
async def save_log_command(interaction: discord.Interaction) -> None:
	if interaction.user.id != DEVELOPER_USER_ID and not is_menu_admin(interaction.user):
		await interaction.response.send_message(
			"서버 관리자 또는 개발자만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return

	try:
		snapshot_path = await asyncio.to_thread(save_log_snapshot)
		await interaction.response.send_message(
			f"로그를 저장했습니다: `{snapshot_path.name}`",
			file=discord.File(str(snapshot_path), filename=snapshot_path.name),
			ephemeral=True,
		)
		logger.info(
			"Discord에서 로그를 저장했습니다: user_id=%s, username=%s",
			interaction.user.id,
			str(interaction.user),
		)
	except (OSError, discord.HTTPException) as error:
		logger.exception("Discord 로그 저장 명령어 처리 실패: %s", error)
		await interaction.response.send_message(
			"로그를 저장하지 못했습니다. 콘솔 로그를 확인해주세요.",
			ephemeral=True,
		)


def make_event_embed(event: dict[str, str]) -> discord.Embed:
	status = "진행중" if str(event.get("status")) == "0" else "종료"
	embed = discord.Embed(
		title=event.get("title", "행사명 없음"),
		url=event.get("submitLink") or BASE_URL,
		color=discord.Color.blue(),
	)
	embed.set_author(name="ComicWorld", icon_url=COMICWORLD_EMOJI_URL)
	embed.add_field(
		name="기간",
		value=f"{event.get('startDate', '-')} ~ {event.get('endDate', '-')}",
		inline=False,
	)
	embed.add_field(name="장소", value=event.get("place", "-"), inline=False)
	if event.get("tag"):
		embed.add_field(name="태그", value=f"#{event['tag']}", inline=True)
	embed.set_footer(text="Comic World 행사정보")
	return embed


def get_nearest_events(events: list[dict[str, str]]) -> list[dict[str, str]]:
	today = date.today()
	upcoming = []
	for event in events:
		try:
			start_date = date.fromisoformat(event["startDate"])
		except (KeyError, ValueError):
			continue
		if start_date >= today:
			upcoming.append((start_date, event))

	if upcoming:
		return [event for _, event in sorted(upcoming, key=lambda item: item[0])]
	return events



@app_commands.command(
	name="문제출제",
	description="문제와 힌트, 최대 4개의 정답을 등록합니다.",
)
@app_commands.describe(
	question="출제할 문제",
	hint="문제의 힌트",
	answers="정답을 쉼표로 구분해 최대 4개 입력 (예: 3, 삼, 셋)",
)
async def submit_quiz_command(
	interaction: discord.Interaction,
	question: str,
	hint: str,
	answers: str,
) -> None:
	if interaction.guild_id is None:
		await interaction.response.send_message(
			"서버에서만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return

	question = question.strip()
	hint = hint.strip()
	answer_list = [answer.strip() for answer in answers.split(",")]
	if not question or not hint or any(not answer for answer in answer_list):
		await interaction.response.send_message(
			"문제, 힌트, 정답을 모두 입력해주세요. 정답은 쉼표로 구분해주세요.",
			ephemeral=True,
		)
		return
	if len(question) > 1000 or len(hint) > 1000:
		await interaction.response.send_message(
			"문제와 힌트는 각각 1000자 이내로 입력해주세요.",
			ephemeral=True,
		)
		return
	if len(answer_list) > QUIZ_MAX_ANSWERS or any(len(answer) > 200 for answer in answer_list):
		await interaction.response.send_message(
			"정답은 최대 4개까지, 각 200자 이내로 입력해주세요.",
			ephemeral=True,
		)
		return
	unique_answers = list(dict.fromkeys(answer_list))
	if len({normalize_quiz_answer(answer) for answer in unique_answers}) != len(unique_answers):
		await interaction.response.send_message(
			"같은 정답은 한 번만 입력해주세요.",
			ephemeral=True,
		)
		return

	await asyncio.to_thread(initialize_menu_db)
	await asyncio.to_thread(
		add_quiz_question,
		interaction.guild_id,
		question,
		hint,
		unique_answers,
		interaction.user.id,
	)
	await interaction.response.send_message(
		"문제를 등록했습니다. `/퀴즈`를 실행하면 등록된 문제를 풀 수 있습니다.",
		ephemeral=True,
	)


@app_commands.command(
	name="퀴즈",
	description="퀴즈를 풀고 정답을 맞혀 레벨 포인트를 얻습니다.",
)
async def quiz_command(interaction: discord.Interaction) -> None:
	if interaction.guild_id is None:
		await interaction.response.send_message(
			"서버에서만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return

	await asyncio.to_thread(initialize_menu_db)
	quiz = await asyncio.to_thread(
		get_random_quiz,
		interaction.guild_id,
		interaction.user.id,
	)
	if quiz is None:
		await interaction.response.send_message(
			"풀 수 있는 문제가 없습니다. 새 문제를 등록하거나 아직 풀지 않은 문제가 있는지 확인해주세요.",
			ephemeral=True,
		)
		return

	remaining = claim_quiz_cooldown()
	if remaining > 0:
		remaining_minutes = math.ceil(remaining / 60)
		await interaction.response.send_message(
			f"퀴즈는 모든 사용자 공통 30분 쿨타임입니다. {remaining_minutes}분 후 다시 시도해주세요.",
			ephemeral=True,
		)
		return

	question_id, question, hint, answers = quiz
	progress = await asyncio.to_thread(get_user_level, interaction.guild_id, interaction.user.id)
	view = QuizView(
		interaction.guild_id,
		interaction.user.id,
		question_id,
		question,
		hint,
		answers,
		progress,
		public=True,
	)
	await interaction.response.send_message(
		embed=make_quiz_embed(question, answers, *progress, show_progress=False),
		view=view,
		ephemeral=False,
	)
	view.message = await interaction.original_response()


@app_commands.command(
	name="문제초기화",
	description="서버에 등록된 퀴즈 문제를 모두 삭제합니다. 관리자 전용.",
)
async def reset_quiz_questions_command(interaction: discord.Interaction) -> None:
	if interaction.guild_id is None:
		await interaction.response.send_message(
			"서버에서만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return
	if not is_menu_admin(interaction.user):
		await interaction.response.send_message(
			"서버 관리자 또는 설정된 관리자만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return

	await asyncio.to_thread(initialize_menu_db)
	removed_count = await asyncio.to_thread(clear_quiz_questions, interaction.guild_id)
	await interaction.response.send_message(
		f"서버의 퀴즈 문제 {removed_count}개를 삭제했습니다. 레벨과 포인트는 유지됩니다.",
		ephemeral=True,
	)


@app_commands.command(
	name="내레벨",
	description="내 레벨과 다음 레벨까지 필요한 포인트를 확인합니다.",
)
async def my_level_command(interaction: discord.Interaction) -> None:
	if interaction.guild_id is None:
		await interaction.response.send_message(
			"서버에서만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return

	await asyncio.to_thread(initialize_menu_db)
	progress = await asyncio.to_thread(
		get_user_level,
		interaction.guild_id,
		interaction.user.id,
	)
	await interaction.response.send_message(
		embed=make_level_embed(interaction.user.display_name, progress),
		ephemeral=True,
	)


@app_commands.command(
	name="메뉴추가",
	description="메뉴를 등록합니다.",
)

@app_commands.describe(menu="등록할 메뉴 문자열")
async def add_menu_command(
	interaction: discord.Interaction,
	menu: str,
) -> None:
	if interaction.guild_id is None:
		await interaction.response.send_message(
			"서버에서만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return

	menu = menu.strip()
	if not menu:
		await interaction.response.send_message(
			"등록할 메뉴를 입력해주세요.",
			ephemeral=True,
		)
		return
	if len(menu) > 100:
		await interaction.response.send_message(
			"메뉴는 100자 이내로 입력해주세요.",
			ephemeral=True,
		)
		return

	await asyncio.to_thread(initialize_menu_db)
	was_added = await asyncio.to_thread(add_menu, interaction.guild_id, menu, interaction.user.id)
	logger.info(
		"메뉴 등록: guild_id=%s, user_id=%s, username=%s, menu=%s, added=%s",
		interaction.guild_id,
		interaction.user.id,
		str(interaction.user),
		menu,
		was_added,
	)
	message = (
		f"`{menu}` 메뉴를 등록했습니다."
		if was_added
		else f"`{menu}` 메뉴는 이미 등록되어 있습니다."
	)
	await interaction.response.send_message(message, ephemeral=True)


@app_commands.command(
	name="메뉴목록",
	description="등록된 메뉴를 목록으로 보여줍니다.",
)
async def list_menus_command(interaction: discord.Interaction) -> None:
	if interaction.guild_id is None:
		await interaction.response.send_message(
			"서버에서만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return

	await asyncio.to_thread(initialize_menu_db)
	menus = await asyncio.to_thread(get_menu_entries, interaction.guild_id)
	if not menus:
		await interaction.response.send_message(
			"등록된 메뉴가 없습니다. `/메뉴추가`로 메뉴를 먼저 등록해주세요.",
			ephemeral=True,
		)
		return

	view = MenuListView(menus, interaction.user.id)
	await interaction.response.send_message(
		embed=make_menu_list_embed(menus),
		view=view,
		ephemeral=True,
	)


class MenuDeleteModal(discord.ui.Modal, title="메뉴 삭제"):
	def __init__(self, guild_id: int) -> None:
		super().__init__()
		self.guild_id = guild_id
		self.menu_name = discord.ui.TextInput(
			label="삭제할 메뉴 이름",
			placeholder="정확한 메뉴 이름을 입력하세요",
			max_length=100,
		)
		self.add_item(self.menu_name)

	async def on_submit(self, interaction: discord.Interaction) -> None:
		menu = self.menu_name.value.strip()
		if not menu:
			await interaction.response.send_message(
				"삭제할 메뉴 이름을 입력해주세요.",
				ephemeral=True,
			)
			return
		is_admin = is_menu_admin(interaction.user)
		deleted = await asyncio.to_thread(
			delete_menu,
			self.guild_id,
			menu,
			interaction.user.id,
			is_admin,
		)
		if deleted:
			message = f"`{menu}` 메뉴를 삭제했습니다."
		else:
			message = (
				f"`{menu}` 메뉴를 찾을 수 없거나, 본인이 등록한 메뉴만 삭제할 수 있습니다."
				if not is_admin
				else f"`{menu}` 메뉴를 찾을 수 없습니다."
			)
		await interaction.response.send_message(message, ephemeral=True)


@app_commands.command(
	name="메뉴삭제",
	description="등록된 메뉴를 삭제합니다.",
)
async def delete_menu_command(interaction: discord.Interaction) -> None:
	if interaction.guild_id is None:
		await interaction.response.send_message(
			"서버에서만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return

	await asyncio.to_thread(initialize_menu_db)
	menus = await asyncio.to_thread(get_menu_entries, interaction.guild_id)
	if not menus:
		await interaction.response.send_message(
			"등록된 메뉴가 없습니다. `/메뉴추가`로 메뉴를 먼저 등록해주세요.",
			ephemeral=True,
		)
		return

	menu_list = "\n".join(f"- {menu}" for menu in menus)
	view = discord.ui.View(timeout=120)

	async def open_delete_modal(interaction: discord.Interaction) -> None:
		await interaction.response.send_modal(MenuDeleteModal(interaction.guild_id or 0))

	button = discord.ui.Button(
		label="삭제할 메뉴 입력",
		style=discord.ButtonStyle.danger,
	)
	button.callback = open_delete_modal
	view.add_item(button)

	await interaction.response.send_message(
		f"현재 등록된 메뉴입니다:\n{menu_list}\n\n삭제할 메뉴를 입력하려면 아래 버튼을 눌러주세요.",
		view=view,
		ephemeral=True,
	)


@app_commands.command(
	name="메뉴초기화",
	description="서버의 모든 메뉴를 삭제합니다. 관리자 전용.",
)
async def reset_menus_command(interaction: discord.Interaction) -> None:
	if interaction.guild_id is None:
		await interaction.response.send_message(
			"서버에서만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return

	if not is_menu_admin(interaction.user):
		await interaction.response.send_message(
			"관리자만 사용할 수 있는 명령어입니다. (서버 관리자 또는 MENU_ADMIN_IDS 설정 사용자)",
			ephemeral=True,
		)
		return

	await asyncio.to_thread(initialize_menu_db)
	removed_count = await asyncio.to_thread(clear_menus, interaction.guild_id)
	await interaction.response.send_message(
		f"서버의 등록 메뉴 {removed_count}개를 삭제했습니다.",
		ephemeral=True,
	)


@app_commands.command(
	name="메뉴추천",
	description="등록된 메뉴 중 하나를 랜덤으로 추천합니다.",
)
async def recommend_menu_command(interaction: discord.Interaction) -> None:
	if interaction.guild_id is None:
		await interaction.response.send_message(
			"서버에서만 사용할 수 있는 명령어입니다.",
			ephemeral=True,
		)
		return

	await asyncio.to_thread(initialize_menu_db)
	menu, menu_count = await asyncio.to_thread(
		get_random_menu,
		interaction.guild_id,
	)
	if menu is None:
		await interaction.response.send_message(
			"등록된 메뉴가 없습니다. `/메뉴추가`로 메뉴를 먼저 등록해주세요.",
			ephemeral=True,
		)
		return

	await interaction.response.send_message(
		format_menu_recommendation(menu),
	)


@app_commands.command(
	name="문의",
	description="개발자에게 문의 내용을 전달합니다. 이미지 첨부 필수입니다.",
)
@app_commands.describe(
	content="문의 내용을 입력하세요",
	attachment="오류/화면 자료 이미지 첨부 (필수)",
)
async def inquiry_command(
	interaction: discord.Interaction,
	content: str,
	attachment: discord.Attachment,
) -> None:
	message = content.strip()
	if not message:
		await interaction.response.send_message(
			"문의 내용을 입력해주세요.",
			ephemeral=True,
		)
		return
	if len(message) > 1000:
		await interaction.response.send_message(
			"문의는 1000자 이내로 입력해주세요.",
			ephemeral=True,
		)
		return
	if attachment is None or not attachment.content_type or not attachment.content_type.startswith("image/"):
		await interaction.response.send_message(
			"문제 화면 또는 오류 이미지 첨부가 필수입니다. 이미지 파일을 함께 보내주세요.",
			ephemeral=True, 	
		)
		return
	developer_user_id = 924576483333259294 #nikuyi_aaaa
	if developer_user_id <= 0:
		await interaction.response.send_message(
			"관리자 DM 전송 대상이 설정되지 않았습니다. 관리자에게 문의해주세요.",
			ephemeral=True,
		)
		logger.warning("관리자 DM 대상이 설정되지 않아 문의 전송이 실패했습니다.")
		return
	logger.info(
		"문의 접수: user_id=%s, username=%s, guild_id=%s, attachment=%s, size=%s, developer_user_id=%s",
		interaction.user.id,
		str(interaction.user),
		interaction.guild_id,
		attachment.url,
		attachment.size,
		developer_user_id,
	)

	try:
		developer = await interaction.client.fetch_user(developer_user_id)
		embed = discord.Embed(
			title="새 문의가 도착했습니다",
			color=discord.Color.orange(),
			description=message,
		)
		embed.add_field(
			name="보낸 사용자",
			value=f"{interaction.user} ({interaction.user.id})",
			inline=False,
		)
		embed.add_field(
			name="서버",
			value=f"{interaction.guild.name if interaction.guild else 'DM'}",
			inline=False,
		)
		embed.add_field(
			name="서버 ID",
			value=str(interaction.guild_id) if interaction.guild_id is not None else "DM",
			inline=False,
		)
		file = await attachment.to_file()
		sent = False
		mention_text = f"<@{developer_user_id}>"
		try:
			dm_channel = await developer.create_dm()
			await dm_channel.send(f"{mention_text}\n문의가 도착했습니다.", embed=embed, file=file)
			sent = True
			logger.info("문의 DM 전송 완료: target_user_id=%s", developer_user_id)
		except discord.Forbidden:
			admin_channel_id = get_admin_channel_id()
			if admin_channel_id is None:
				raise
			channel = interaction.guild.get_channel(admin_channel_id) if interaction.guild else None
			if channel is None:
				channel = interaction.client.get_channel(admin_channel_id)
			if not isinstance(channel, discord.abc.Messageable):
				raise
			await channel.send(f"{mention_text}\n문의가 도착했습니다.", embed=embed, file=file)
			logger.warning(
				"문의 DM이 차단되어 관리자 채널 %s로 대체 전송했습니다. developer_user_id=%s",
				admin_channel_id,
				developer_user_id,
			)
			sent = True
		if sent:
			await interaction.response.send_message(
				"문의가 관리자에게 전달되었습니다. 화면 자료와 함께 전달되었으며 빠른 시일 내에 답변드리겠습니다.",
				ephemeral=True,
			)
		else:
			await interaction.response.send_message(
				"문의 전송 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
				ephemeral=True,
			)
	except discord.HTTPException as error:
		logger.exception("문의 전송 실패: %s", error)
		await send_error_log_to_developer(interaction.client, error, "문의 DM 전송")
		await interaction.response.send_message(
			"개발자와의 DM이 허용되지 않았습니다. 관리자와 같은 서버에 초대되었는지 확인하거나 관리자 채널 설정을 확인해주세요.",
			ephemeral=True,
		)


@app_commands.command(
	name="코믹인포",
	description="코믹월드 행사정보를 보여줍니다.",
)
async def comic_info_command(interaction: discord.Interaction) -> None:
	await interaction.response.defer()
	try:
		events = await asyncio.to_thread(fetch_events)
		nearest = get_nearest_events(events)[:1]
		if not nearest:
			await interaction.followup.send("현재 등록된 행사가 없습니다.")
			return
		await interaction.followup.send(embed=make_event_embed(nearest[0]))
	except (requests.RequestException, ValueError, KeyError) as error:
		logger.exception("코믹인포 명령어 처리 실패: %s", error)
		await send_error_log_to_developer(interaction.client, error, "코믹인포 명령어")
		await interaction.followup.send(
			"행사정보를 가져오지 못했습니다. 잠시 후 다시 시도해주세요.",
			ephemeral=True,
		)
	


@app_commands.command(
	name="코믹스케줄",
	description="코믹월드 행사 일정을 원하는 개수만큼 보여 줍니다.",
)
@app_commands.describe(count="출력할 행사 개수 (1~10)")
async def comic_schedule_command(
	interaction: discord.Interaction,
	count: app_commands.Range[int, 1, 10],
) -> None:
	global schedule_cooldown_until
	now = time.monotonic()
	if schedule_cooldown_until is not None:
		remaining = schedule_cooldown_until - now
		if remaining > 0:
			try:
				remaining_minutes = math.ceil(remaining / 60)
				await interaction.response.send_message(
					f"이 명령어는 전체 10분 쿨타임이 있습니다. {remaining_minutes}분 후 다시 시도해주세요.",
					ephemeral=True,
				)
			except discord.NotFound:
				logger.warning("쿨타임 안내 전에 상호작용이 만료되었습니다.")
			return

	schedule_cooldown_until = now + SCHEDULE_COOLDOWN_SECONDS
	try:
		await interaction.response.defer()
	except discord.NotFound:
		logger.warning("코믹스케줄 상호작용이 응답 전에 만료되었습니다.")
		return
	try:
		events = await asyncio.to_thread(fetch_events)
		scheduled = get_nearest_events(events)[:count]
		if not scheduled:
			await interaction.followup.send("현재 등록된 행사가 없습니다.")
			return
		await interaction.followup.send(
			content=f"요청한 **{count}개**의 코믹월드 행사 목록입니다.\n-# _전체 {len(events)}개_",
			embeds=[make_event_embed(event) for event in scheduled],
		)
	except (requests.RequestException, ValueError, KeyError) as error:
		logger.exception("코믹스케줄 명령어 처리 실패: %s", error)
		await send_error_log_to_developer(interaction.client, error, "코믹스케줄 명령어")
		try:
			await interaction.followup.send(
				"행사정보를 가져오지 못했습니다. 잠시 후 다시 시도해주세요.",
				ephemeral=True,
			)
		except discord.NotFound:
			logger.warning("오류 안내 전에 코믹스케줄 상호작용이 만료되었습니다.")
class ComicWorldBot(commands.Bot):
	def __init__(self, channel_id: int | None) -> None:
		intents = discord.Intents.default()
		intents.message_content = True
		super().__init__(command_prefix="!", intents=intents)
		self.channel_id = channel_id
		self.login_started_at: float | None = None
		self.commands_synced = False

	async def sync_commands_with_retry(self, max_retries: int = 3) -> None:
		for attempt in range(1, max_retries + 1):
			try:
				for guild in self.guilds:
					self.tree.clear_commands(guild=guild)
					await self.tree.sync(guild=guild)
					logger.info(
						"슬래시 명령어를 서버에 동기화했습니다: guild=%s (%s)",
						guild.name,
						guild.id,
					)
				await self.tree.sync()
				logger.info("전역 슬래시 명령어를 동기화했습니다.")
				self.commands_synced = True
				return
			except discord.Forbidden:
				logger.error(
					"전역 슬래시 명령어 동기화 권한이 없습니다. "
					"봇 초대 URL에 'bot'과 'applications.commands' 권한 범위가 포함되어 있는지 확인하세요."
				)
				return
			except discord.HTTPException as error:
				status_code = getattr(error, "status", None)
				if status_code not in {500, 502, 503, 504}:
					raise
				if attempt == max_retries:
					logger.exception(
						"Discord API가 반복적으로 500 오류를 반환했습니다. 마지막 시도 후 명령어 동기화를 포기합니다.",
					)
					return
				logger.warning(
					"Discord 명령어 동기화에 일시적 %s 오류가 발생해 %d초 뒤 재시도합니다. (%d/%d)",
					status_code,
					attempt,
					attempt,
					max_retries,
				)
				await asyncio.sleep(attempt * 5)

	async def setup_hook(self) -> None:
		self.tree.on_error = self.on_app_command_error
		self.tree.add_command(comic_info_command)
		self.tree.add_command(comic_schedule_command)
		self.tree.add_command(quiz_command)
		self.tree.add_command(submit_quiz_command)
		self.tree.add_command(reset_quiz_questions_command)
		self.tree.add_command(my_level_command)
		self.tree.add_command(add_menu_command)
		self.tree.add_command(list_menus_command)
		self.tree.add_command(delete_menu_command)
		self.tree.add_command(reset_menus_command)
		self.tree.add_command(recommend_menu_command)
		self.tree.add_command(status_command)
		self.tree.add_command(save_log_command)
		self.tree.add_command(inquiry_command)
		self.tree.add_command(help_command)
		self.add_command(butter_command)
		self.add_command(tig_command)
		self.add_command(stop_command)
		initialize_menu_db()
		if self.channel_id is not None:
			self.update_events.start()
		else:
			logger.warning("DISCORD_CHANNEL_ID가 없어 주기 알림을 비활성화합니다.")
		if (
			get_auto_message_times()
			and any(get_auto_message_text(scheduled_time) for scheduled_time in get_auto_message_times())
			and get_auto_message_channel_ids()
		):
			self.send_auto_message.start()
		else:
			logger.info(
				"AUTO_MESSAGE_TIME, AUTO_MESSAGE_TEXTS 또는 AUTO_MESSAGE_CHANNEL_IDS가 없어 "
				"예약 메시지를 비활성화합니다."
			)

	async def on_ready(self) -> None:
		if self.login_started_at is None:
			self.login_started_at = time.monotonic()
		if not self.update_activity.is_running():
			self.update_activity.start()
		if not self.commands_synced:
			await self.sync_commands_with_retry()
		logger.info("로그인 완료: %s", self.user)
		logger.info(BOT_ON_MESSAGE)

	async def on_interaction(self, interaction: discord.Interaction) -> None:
		if interaction.type is not discord.InteractionType.application_command:
			return

		command = interaction.command
		command_name = getattr(command, "qualified_name", None)
		if command_name is None:
			command_name = interaction.data.get("name", "알 수 없음")# type: ignore
		logger.info(
			"CommandTriggered: , command:%s, user_id=%s, username=%s",
			command_name,
			interaction.user.id,
			str(interaction.user),
		)

	async def on_command_error(
		self,
		ctx: commands.Context,
		error: commands.CommandError,
	) -> None:
		if isinstance(error, commands.CommandNotFound):
			return

		logger.exception("일반 명령어 처리 중 오류가 발생했습니다: %s", error)
		await send_error_log_to_developer(
			self,
			error,
			f"일반 명령어: {getattr(ctx.command, 'qualified_name', '알 수 없음')}",
			format_error_traceback(error),
		)

	async def on_app_command_error(
		self,
		interaction: discord.Interaction,
		error: app_commands.AppCommandError,
	) -> None:
		logger.exception("슬래시 명령어 처리 중 오류가 발생했습니다: %s", error)
		await send_error_log_to_developer(
			self,
			error,
			f"슬래시 명령어: {getattr(interaction.command, 'name', '알 수 없음')}",
			format_error_traceback(error),
		)
		if not interaction.response.is_done():
			await interaction.response.send_message(
				"명령어 처리 중 오류가 발생했습니다. 개발자에게 오류 로그를 자동 전송했습니다.",
				ephemeral=True,
			)

	async def on_error(self, event_method: str, *args, **kwargs) -> None:
		error = sys.exc_info()[1] or RuntimeError("알 수 없는 Discord 이벤트 오류")
		logger.exception("Discord 이벤트 처리 중 오류가 발생했습니다: %s", event_method)
		await send_error_log_to_developer(
			self,
			error,
			f"Discord 이벤트: {event_method}",
			format_error_traceback(error),
		)

	@tasks.loop(minutes=1)
	async def update_activity(self) -> None:
		global activity_change_count, activity_current_text, activity_next_change_at, activity_period

		now = datetime.now(KST)
		current_period = get_activity_period(now)
		if current_period is None:
			if activity_period is not None or activity_current_text is not None:
				await self.change_presence(activity=None)
				logger.info("상태 메시지를 제거했습니다: time=%s", now.strftime("%H:%M"))
			activity_period = None
			activity_change_count = 0
			activity_current_text = None
			activity_next_change_at = None
			return

		if current_period != activity_period:
			activity_period = current_period
			activity_change_count = 0
			activity_current_text = choose_activity_text(current_period)
			await self.change_presence(activity=discord.Game(name=activity_current_text))
			delay_hours = get_activity_change_delay_hours()
			activity_next_change_at = now + timedelta(hours=delay_hours)
			logger.info(
				"상태 메시지를 변경했습니다: period=%s, text=%s, next_change_in=%.1f시간",
				current_period,
				activity_current_text,
				delay_hours,
			)
			return

		if (
			activity_change_count >= 3
			or activity_next_change_at is None
			or now < activity_next_change_at
		):
			return

		activity_current_text = choose_activity_text(current_period, activity_current_text)
		activity_change_count += 1
		await self.change_presence(activity=discord.Game(name=activity_current_text))
		delay_hours = get_activity_change_delay_hours()
		activity_next_change_at = now + timedelta(hours=delay_hours)
		logger.info(
			"상태 메시지를 변경했습니다: period=%s, text=%s, change_count=%d, next_change_in=%.1f시간",
			current_period,
			activity_current_text,
			activity_change_count,
			delay_hours,
		)

	@update_activity.before_loop
	async def before_update_activity(self) -> None:
		await self.wait_until_ready()

	@tasks.loop(minutes=float(os.getenv("POLL_MINUTES", "30")))
	async def update_events(self) -> None:
		if self.channel_id is None:
			return
		channel = self.get_channel(self.channel_id)
		if not isinstance(channel, discord.abc.Messageable):
			logger.error("채널을 찾을 수 없습니다: %s", self.channel_id)
			return

		try:
			events = await asyncio.to_thread(fetch_events)
			fingerprint = events_fingerprint(events)
			if fingerprint == load_cached_fingerprint():
				logger.info("행사정보 변경 없음")
				return

			embeds = [make_event_embed(event) for event in events[:10]]
			if embeds:
				await channel.send(
					content="코믹월드 행사정보가 업데이트되었습니다.",
					embeds=embeds,
				)
			save_cached_fingerprint(fingerprint)
			logger.info("행사정보 %d건 전송 완료", len(embeds))
		except (requests.RequestException, ValueError, KeyError) as error:
			logger.exception("행사정보를 가져오지 못했습니다: %s", error)
			await send_error_log_to_developer(self, error, "행사정보 주기 업데이트")

	@tasks.loop(minutes=1)
	async def send_auto_message(self) -> None:
		scheduled_times = get_auto_message_times()
		channel_ids = get_auto_message_channel_ids()
		if not scheduled_times or not channel_ids:
			return

		now = datetime.now(KST)
		current_time = (now.hour, now.minute)
		if current_time not in scheduled_times or not is_auto_message_day_allowed(current_time, now.weekday()):
			return
		message = get_auto_message_text(current_time)
		if message is None:
			return

		for channel_id in channel_ids:
			if last_auto_message_dates.get(channel_id) == now.date():
				continue
			channel = self.get_channel(channel_id)
			if channel is None:
				try:
					channel = await self.fetch_channel(channel_id)
				except (discord.NotFound, discord.Forbidden, discord.HTTPException) as error:
					logger.exception("예약 메시지 채널 조회 실패: channel_id=%s, error=%s", channel_id, error)
					await send_error_log_to_developer(self, error, f"예약 메시지 채널 조회: {channel_id}")
					continue
			if not isinstance(channel, discord.abc.Messageable):
				logger.error("예약 메시지 채널을 찾을 수 없습니다: %s", channel_id)
				continue
			try:
				await channel.send(message)
				last_auto_message_dates[channel_id] = now.date()
				logger.info("예약 메시지를 전송했습니다: channel_id=%s, time=%s", channel_id, current_time)
			except discord.HTTPException as error:
				logger.exception("예약 메시지 전송 실패: channel_id=%s, error=%s", channel_id, error)
				await send_error_log_to_developer(self, error, f"예약 메시지 전송: {channel_id}")

	@send_auto_message.before_loop
	async def before_send_auto_message(self) -> None:
		await self.wait_until_ready()

	@update_events.before_loop
	async def before_update_events(self) -> None:
		await self.wait_until_ready()


def main() -> None:
	token = required_env("DISCORD_TOKEN")
	channel_id_value = os.getenv("DISCORD_CHANNEL_ID")
	channel_id = int(channel_id_value) if channel_id_value else None
	bot = ComicWorldBot(channel_id)
	start_console_command_listener()
	bot.run(token)


if __name__ == "__main__":
	main()