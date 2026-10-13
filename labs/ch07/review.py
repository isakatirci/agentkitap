"""Savunmaci agent review.

Bu fonksiyon saldiri uretmez. Eksik siniri isimlendirir.
On soruluk ders review'u bu kontrollerin etrafinda anlatilir.
"""


def review_agent(config: dict) -> list[str]:
    """Eksik savunmalari madde madde dondurur. Bos liste, bu kontrol listesini gecer."""

    findings: list[str] = []
    if not config.get("sandbox"):
        findings.append("filesystem is not sandboxed")
    if not config.get("system_prompt"):
        findings.append("system prompt is missing")
    if not config.get("untrusted_text_is_data"):
        findings.append("prompt injection: untrusted text can override the system prompt")
    if config.get("tools_from_untrusted_server"):
        findings.append("supply chain: tools come from an untrusted server")
    if config.get("skills_or_mcp_run_code") and not config.get("sandbox"):
        findings.append("skills or MCP servers would run code outside a sandbox")
    return findings


def main() -> list[str]:
    unsafe = {
        "sandbox": False,
        "system_prompt": "",
        "untrusted_text_is_data": False,
        "tools_from_untrusted_server": True,
        "skills_or_mcp_run_code": True,
    }
    findings = review_agent(unsafe)
    for item in findings:
        print(item)
    return findings


if __name__ == "__main__":
    main()
