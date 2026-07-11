"""One-time script to update existing KB articles with 2026-06-24 daily log data."""
import os

base = "/home/nel/claude-memory-compiler/knowledge/concepts"


def update_nanabanana():
    path = os.path.join(base, "nanabanana-project.md")
    with open(path, "r") as f:
        content = f.read()

    content = content.replace(
        '  - "daily/2026-06-23.md"\ncreated: 2026-05-15\nupdated: 2026-06-23',
        '  - "daily/2026-06-23.md"\n  - "daily/2026-06-24.md"\ncreated: 2026-05-15\nupdated: 2026-06-24',
    )

    new_section = (
        "### P3 Security Audit (24 июня 2026)\n\n"
        "7x queryRawUnsafe заменены на queryRaw tagged template в finance.controller.ts. "
        "TTL magic-link 900->600с. Два пункта уже закрыты (.unref, .catch). "
        "Отложен DI для PrismaClient.\n\n"
        "### Pollinations Failover (24 июня 2026)\n\n"
        "Добавлен Pollinations (FLUX.1-dev) как 4-е non-Google звено failover. "
        "Text-to-image only, без API-ключа. Prisma enum ApiProvider расширен.\n\n"
        "### CAS Idempotent Refund (24 июня 2026)\n\n"
        "Race condition двойного refund закрыта: isRefunded Boolean + updateMany CAS.\n\n"
        "### Redis Dashboard Caching (24 июня 2026)\n\n"
        "Redis-кэш dashboard (TTL 120с) и report (TTL 300с). Graceful degradation.\n\n"
        "### Prisma Select Optimization (24 июня 2026)\n\n"
        "include->select в users.controller.ts: width 898->698 байт.\n\n"
    )

    content = content.replace(
        "## Related Concepts\n\n- [[concepts/jwt-hardening]]",
        new_section + "## Related Concepts\n\n- [[concepts/jwt-hardening]]",
    )

    content = content.replace(
        "- [[concepts/token-encryption-key-separation]] — Разделение ключа шифрования T-Bank от JWT-секрета",
        "- [[concepts/token-encryption-key-separation]] — Разделение ключа шифрования T-Bank от JWT-секрета\n"
        "- [[concepts/pollinations-failover-provider]] — 4-е non-Google звено failover генерации\n"
        "- [[concepts/cas-idempotent-refund]] — CAS через isRefunded\n"
        "- [[concepts/redis-dashboard-caching]] — Redis-кэш дашборда\n"
        "- [[concepts/prisma-query-raw-safety]] — queryRawUnsafe->queryRaw",
    )

    content = content.replace(
        "- [[daily/2026-06-23.md]] — Зависание бота 12 мин",
        "- [[daily/2026-06-24.md]] — P3 аудит; Pollinations failover; CAS refund; Redis cache; select optimization\n"
        "- [[daily/2026-06-23.md]] — Зависание бота 12 мин",
    )

    with open(path, "w") as f:
        f.write(content)
    print("Updated nanabanana-project.md")


def update_mvp_bonds():
    path = os.path.join(base, "mvp-bonds-project.md")
    with open(path, "r") as f:
        content = f.read()

    content = content.replace(
        '  - "daily/2026-06-23.md"\ncreated: 2026-05-29\nupdated: 2026-06-23',
        '  - "daily/2026-06-23.md"\n  - "daily/2026-06-24.md"\ncreated: 2026-05-29\nupdated: 2026-06-24',
    )

    mvp_new = (
        "### Systemd Autodeploy Timer (24 июня 2026)\n\n"
        "Автоматический деплой через systemd timer каждые 5 минут: ops/auto-deploy.sh "
        "делает git fetch -> rev-list сравнение -> deploy.sh -> TG-уведомление. "
        "TG chat_id из SQLite app_settings, bot token из .env.\n\n"
    )

    content = content.replace(
        "## Related Concepts\n\n- [[concepts/cbr-api-integration]]",
        mvp_new + "## Related Concepts\n\n- [[concepts/cbr-api-integration]]",
    )

    content = content.replace(
        "- [[concepts/graceful-ai-degradation]] — Graceful degradation для OpenAI-зависимых методов",
        "- [[concepts/graceful-ai-degradation]] — Graceful degradation для OpenAI-зависимых методов\n"
        "- [[concepts/systemd-autodeploy-timer]] — Автоматический деплой через systemd timer",
    )

    content = content.replace(
        "- [[daily/2026-06-23.md]] — Graceful AI degradation",
        "- [[daily/2026-06-24.md]] — Systemd autodeploy timer: 5 мин, ops/auto-deploy.sh, TG из SQLite\n"
        "- [[daily/2026-06-23.md]] — Graceful AI degradation",
    )

    with open(path, "w") as f:
        f.write(content)
    print("Updated mvp-bonds-project.md")


def update_prof():
    path = os.path.join(base, "prof-dashboard-project.md")
    with open(path, "r") as f:
        content = f.read()

    content = content.replace(
        '  - "daily/2026-06-23.md"\ncreated: 2026-06-21\nupdated: 2026-06-23',
        '  - "daily/2026-06-23.md"\n  - "daily/2026-06-24.md"\ncreated: 2026-06-21\nupdated: 2026-06-24',
    )

    prof_new = (
        "### Системные фиксы ядра (2026-06-24)\n\n"
        "Три проблемы из-за которых карточки ложно падали в failed (инцидент на доске nanabanana): "
        "(1) PATH без nvm в systemd: _nvm_bin() + _run_bash_lc(). "
        "(2) Slug карты stale при переносе: _card_board_slug() через JOIN boards. "
        "(3) Пустой diff = провал: маркер no_git_changes=True, статус needs_input. "
        "195/195 тестов.\n\n"
    )

    content = content.replace(
        "### Технические решения\n",
        prof_new + "### Технические решения\n",
    )

    content = content.replace(
        "- [[concepts/prof-prod-audit]] — Prod-audit",
        "- [[concepts/prof-prod-audit]] — Prod-audit\n"
        "- [[concepts/prof-systemd-environment]] — Фиксы nvm PATH, slug, пустого diff",
    )

    content = content.replace(
        "- [[daily/2026-06-23.md]] — Deploy detection",
        "- [[daily/2026-06-24.md]] — 3 системных фикса: _nvm_bin, _card_board_slug, no_git_changes; 195 тестов\n"
        "- [[daily/2026-06-23.md]] — Deploy detection",
    )

    with open(path, "w") as f:
        f.write(content)
    print("Updated prof-dashboard-project.md")


def update_ai_failover():
    path = os.path.join(base, "ai-image-generation-failover.md")
    with open(path, "r") as f:
        content = f.read()

    content = content.replace(
        'sources:\n  - "daily/2026-05-18.md"\ncreated: 2026-05-18\nupdated: 2026-05-18',
        'sources:\n  - "daily/2026-05-18.md"\n  - "daily/2026-06-24.md"\ncreated: 2026-05-18\nupdated: 2026-06-24',
    )

    failover_new = (
        "### Pollinations как 4-е звено (2026-06-24)\n\n"
        "Все три звена failover-цепочки используют Google-модели — единая content policy. "
        "Добавлен Pollinations (FLUX.1-dev) как 4-е non-Google звено: без API-ключа, "
        "своя content policy, text-to-image only. Активируется при тройном Google-блоке.\n\n"
    )

    content = content.replace(
        "## Related Concepts\n\n- [[concepts/nanabanana-project]]",
        failover_new + "## Related Concepts\n\n- [[concepts/nanabanana-project]]",
    )

    content = content.replace(
        "- [[concepts/geo-tunnel-for-ai-apis]] — Туннелирование для обхода geo-ограничений основного провайдера",
        "- [[concepts/geo-tunnel-for-ai-apis]] — Туннелирование для обхода geo-ограничений основного провайдера\n"
        "- [[concepts/pollinations-failover-provider]] — Pollinations (FLUX.1-dev) как 4-е non-Google звено",
    )

    content = content.replace(
        "## Sources\n\n- [[daily/2026-05-18.md]]",
        "## Sources\n\n- [[daily/2026-06-24.md]] — Добавление Pollinations как 4-го non-Google звена\n- [[daily/2026-05-18.md]]",
    )

    with open(path, "w") as f:
        f.write(content)
    print("Updated ai-image-generation-failover.md")


def update_prisma_serializable():
    path = os.path.join(base, "prisma-serializable-transactions.md")
    with open(path, "r") as f:
        content = f.read()

    content = content.replace(
        'sources:\n  - "daily/2026-05-31.md"\ncreated: 2026-05-31\nupdated: 2026-05-31',
        'sources:\n  - "daily/2026-05-31.md"\n  - "daily/2026-06-24.md"\ncreated: 2026-05-31\nupdated: 2026-06-24',
    )

    prisma_new = (
        "### CAS как замена Serializable (2026-06-24)\n\n"
        "Для идемпотентных операций (refund токенов) CAS через updateMany + count-check "
        "надёжнее Serializable-транзакции: один атомарный UPDATE без окна между SELECT и UPDATE. "
        "isRefunded Boolean + updateMany WHERE isRefunded:false заменил txSerializable "
        "для refundTokens и recoverStaleGeneration.\n"
    )

    content = content.replace(
        "## Related Concepts",
        prisma_new + "\n## Related Concepts",
    )

    content = content.replace(
        "- [[concepts/yookassa-payment-behavior]] — ЮKassa webhook'и",
        "- [[concepts/yookassa-payment-behavior]] — ЮKassa webhook'и\n"
        "- [[concepts/cas-idempotent-refund]] — CAS через isRefunded заменяет txSerializable для refund",
    )

    content = content.replace(
        "## Sources\n\n- [[daily/2026-05-31.md]]",
        "## Sources\n\n- [[daily/2026-06-24.md]] — CAS updateMany+isRefunded как замена txSerializable\n- [[daily/2026-05-31.md]]",
    )

    with open(path, "w") as f:
        f.write(content)
    print("Updated prisma-serializable-transactions.md")


if __name__ == "__main__":
    update_nanabanana()
    update_mvp_bonds()
    update_prof()
    update_ai_failover()
    update_prisma_serializable()
    print("\nAll articles updated successfully")
