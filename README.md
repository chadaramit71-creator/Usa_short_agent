# USA Short Agent

A starter automation project for USA Facts and Mystery YouTube Shorts. It creates a vertical MP4 with original graphic cards, English narration, and metadata. GitHub Actions runs twice daily and saves output as a downloadable artifact.

## Start from Android

1. Open the **Actions** tab in this repository.
2. Enable GitHub Actions if prompted.
3. Open **Generate USA Shorts** and tap **Run workflow**.
4. Wait for the run to finish, open it, and download the `usa-short-...` artifact.
5. Open the ZIP on your phone and review the video.

The schedule is 14:00 and 22:00 UTC daily (19:30 and 03:30 India time). Scheduled workflows can be delayed or disabled by GitHub if a repository is inactive.

## Optional YouTube upload

You must configure Google/YouTube API OAuth first. Add these repository Actions secrets:
- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

The refresh token must have the `youtube.upload` scope. The included uploader uploads videos as **private** so you can review them first. Never put credentials in source files or commit them.

## Limitations

- This starter creates simple text-card videos, not cinematic footage.
- gTTS needs internet access and uses an online service.
- Verify all factual claims and source notes before publishing.
- Free quotas, API verification, TTS availability, and GitHub Actions limits can affect runs.
- Add original commentary and meaningful editing; avoid repetitive, low-value mass uploads that may violate YouTube policies.
