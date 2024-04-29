from domain.repositories.db_repo.requests import RequestsRepo


async def format_statistics_info(
        repo: RequestsRepo
) -> str:
    total_users_count = await repo.users.get_users_count()
    ru_users_count = await repo.users.get_users_count_by_language(language_code="ru")
    uz_users_count = await repo.users.get_users_count_by_language(language_code="uz")
    en_users_count = await repo.users.get_users_count_by_language(language_code="en")

    text = (
        f"Всего пользователей: <b>{total_users_count}</b> чел.\n"
        f"Распределение по языкам:\n"
        f"🇷🇺: <b>{ru_users_count}</b> чел. <b>~{int(ru_users_count / total_users_count * 100)}%</b>\n"
        f"🇺🇿: <b>{uz_users_count}</b> чел. <b>~{int(uz_users_count / total_users_count * 100)}%</b>\n"
        f"🇬🇧: <b>{en_users_count}</b> чел. <b>~{int(en_users_count / total_users_count * 100)}%</b>\n"
    )

    return text
