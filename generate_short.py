import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

OUT = Path("output")
FRAMES = OUT / "frames"
OUT.mkdir(exist_ok=True)
FRAMES.mkdir(exist_ok=True)

TOPICS = [
    {"title":"WHY IS ALASKA SO HUGE?","hook":"Here is a surprising fact about the United States.",
     "lines":["Alaska is the largest U.S. state by area.","It is bigger than Texas, California, and Montana combined.",
              "Yet much of Alaska has a very low population density.","Would you visit America's biggest state?"],
     "source":"Source to verify: U.S. Census Bureau and Alaska state statistics."},
    {"title":"THE MYSTERY OF DEATH VALLEY","hook":"One of America's strangest places is Death Valley.",
     "lines":["Death Valley is famous for extreme desert heat.","Rocks in Racetrack Playa have left long trails across the ground.",
              "Scientists found that thin sheets of ice and wind can move them.","A mystery explained by nature!"],
     "source":"Source to verify: National Park Service, Death Valley National Park."},
    {"title":"WHY DOES THE U.S. HAVE 4 TIME ZONES?","hook":"The United States can have different times at the same moment.",
     "lines":["The contiguous United States spans four main time zones.","They are Eastern, Central, Mountain, and Pacific.",
              "Alaska and Hawaii have their own time zones too.","That is why a live event can start at different local times."],
     "source":"Source to verify: U.S. Department of Transportation."},
    {"title":"THE GRAND CANYON'S DEEP STORY","hook":"This famous American landscape took a very long time to form.",
     "lines":["The Grand Canyon is in Arizona.","The Colorado River and erosion helped carve the landscape.",
              "Its rock layers reveal a long record of Earth's history.","Would you watch sunrise from the canyon rim?"],
     "source":"Source to verify: National Park Service, Grand Canyon National Park."}
]

def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def wrap(draw, text, fnt, max_width):
    words, lines, current = text.split(), [], ""
    for word in words:
        test = (current + " " + word).strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def make_frame(index, topic, text, label):
    w, h = 720, 1280
    im = Image.new("RGB", (w, h), (10, 23, 48))
    d = ImageDraw.Draw(im)
    for y in range(h):
        t = y / h
        d.line((0, y, w, y), fill=(int(10+12*t), int(23+18*t), int(48+30*t)))
    d.ellipse((420, 80, 820, 480), fill=(22, 57, 91))
    d.ellipse((-180, 820, 260, 1260), fill=(19, 45, 76))
    d.rounded_rectangle((38, 50, w-38, 116), radius=22, fill=(210, 35, 52))
    d.text((w//2, 83), "USA FACTS  •  MYSTERIES", font=font(25, True), anchor="mm", fill="white")
    d.text((w//2, 210), topic, font=font(32, True), anchor="mm", fill=(255, 210, 80), align="center")
    lines = wrap(d, text, font(43, True), w-100)
    line_h = 62
    start_y = 470 - (len(lines)*line_h)//2
    for j, line in enumerate(lines):
        d.text((w//2, start_y+j*line_h), line, font=font(43, True), anchor="mm",
               fill="white", stroke_width=1, stroke_fill=(0,0,0))
    d.rounded_rectangle((55, 1040, w-55, 1120), radius=18, outline=(255,210,80), width=3)
    d.text((w//2, 1080), label, font=font(24, True), anchor="mm", fill=(255,210,80))
    d.text((w//2, 1205), "FOLLOW FOR MORE AMERICAN FACTS", font=font(20, True), anchor="mm", fill=(215,225,240))
    im.save(FRAMES / f"frame_{index:03d}.png")

def main():
    run_index = int(os.getenv("GITHUB_RUN_NUMBER", "1"))
    topic = TOPICS[(run_index - 1) % len(TOPICS)]
    narration = " ".join([topic["hook"]] + topic["lines"] + ["Follow for more USA facts and mysteries."])
    audio = OUT / "voice.mp3"
    gTTS(text=narration, lang="en", slow=False).save(str(audio))
    slides = [topic["hook"]] + topic["lines"] + ["Follow for more!"]
    for i, text in enumerate(slides):
        make_frame(i, topic["title"], text, f"FACT {i+1}/{len(slides)}")
    concat = OUT / "frames.txt"
    with concat.open("w", encoding="utf-8") as f:
        for i in range(len(slides)):
            f.write(f"file 'frames/frame_{i:03d}.png'\n")
            f.write("duration 5\n")
        f.write(f"file 'frames/frame_{len(slides)-1:03d}.png'\n")
    video = OUT / "usa_short.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-i", str(audio), "-vf", "scale=720:1280,format=yuv420p",
        "-c:v", "libx264", "-preset", "ultrafast", "-r", "30",
        "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart",
        str(video)
    ], check=True)
    description = topic["source"] + "\n\nPlease verify factual claims before publishing.\n#USAFacts #Mystery #Shorts"
    (OUT / "metadata.txt").write_text(
        "TITLE: " + topic["title"].title() + " #Shorts\n\nDESCRIPTION:\n" + description +
        "\n\nNARRATION:\n" + narration + "\n", encoding="utf-8")
    print(f"Created {video}")

if __name__ == "__main__":
    main()
