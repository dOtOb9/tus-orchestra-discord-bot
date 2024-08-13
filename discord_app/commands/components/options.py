import discord


class YearOption(discord.Option):
    def __init__(self, **kwargs):
        super().__init__(int, min_value=2024, max_value=2100, description=kwargs['add_desc'] + "何年かを入力してください。", **kwargs)

class MonthOption(discord.Option):
    def __init__(self, **kwargs):
        super().__init__(int, max_value=12, min_value=1, description=kwargs['add_desc'] + "何月かを入力してください。", **kwargs)


class DayOption(discord.Option):
    def __init__(self, **kwargs):
        super().__init__(int, min_value=1, max_value=31, description=kwargs['add_desc'] + "何日かを入力してください。", **kwargs)


class HourOption(discord.Option):
    def __init__(self, **kwargs):
        super().__init__(int, max_value=23, min_value=0, description=kwargs['add_desc'] + "何時かを入力してください。", **kwargs)


class MinuteOption(discord.Option):
    def __init__(self, **kwargs):
        super().__init__(int, min_value=0, max_value=59, description=kwargs['add_desc'] + "何分かを入力してください。", **kwargs)


class SendTypeOption(discord.Option):
    def __init__(self, **kwargs):
        super().__init__(str, choices=["Cc", "Bcc"], description="送信先を表示可とする場合は`Cc`、それ以外は`Bcc`と入力してください。", **kwargs)


class CampusOption(discord.Option):
    def __init__(self):
        super().__init__(str, choices=['野田', '葛飾', '神楽坂'], description="キャンパスを選択してください。")

class TrainingOption(discord.Option):
    def __init__(self):
        super().__init__(str, choices=["前曲", "中曲", "メイン曲", "無し"], description="練習曲を選択してください。")