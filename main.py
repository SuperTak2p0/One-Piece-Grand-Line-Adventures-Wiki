import wiki_updater

def main():
    print("Hello from repl-nix-workspace!")
    updater = wiki_updater.WikiUpdater()
    updater.release_feature(
        feature_name="Races",
        description="Choose your race and start your journey, with common and very rare races that each offer unique abilities and playstyles.",
        release_date="2025-06-01",
        mod_version="1.2.0",
        under_editing=True
    )

if __name__ == "__main__":
    main()
