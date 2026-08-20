fn main() -> anyhow::Result<()> {
    let mut set_token = false;
    for argument in std::env::args() {
        if argument == "--set-token" {
            set_token = true;
        }

        if set_token {
            let contents = format!("TELOXIDE_TOKEN={argument}");
            std::fs::write("./.env", contents)?;
        }
    }

    Ok(())
}
