import wiki_updater

def main():
    print("Hello from repl-nix-workspace!")
    updater = wiki_updater.WikiUpdater()
    updater.release_feature(
        feature_name="Factions",
        description="Align with the Marines, join a Pirate Crew, or work for the World Government — your choice.",
        icon= "🤝"
    )


if __name__ == "__main__":
    main()
