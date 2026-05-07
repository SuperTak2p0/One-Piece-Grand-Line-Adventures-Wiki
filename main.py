import wiki_updater

def main():
    print("Hello from repl-nix-workspace!")
    updater = wiki_updater.WikiUpdater()
    updater.release_feature(
        feature_name="Factions",
        description="Align with the Marines, join a Pirate Crew, or work for the World Government — your choice.",
        release_date="Apr 29, 2026",
        mod_version="1.1.4",
        under_editing=True
    )


if __name__ == "__main__":
    main()
