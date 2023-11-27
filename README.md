# Audio Quality Quiz

## Description

The Audio Quality Quiz is a Python application that challenges users to identify the highest quality audio clip among a set of options. Users can also add their own questions to the quiz, including the option to display an album cover with each question.

## Requirements

- Python 3.x
- Pygame
- PIL (Python Imaging Library)
- Tkinter

## Installation

1. **Python Installation**: Make sure Python 3.x is installed on your system. If not, download and install it from [Python's official website](https://www.python.org/downloads/).

2. **Library Installation**: Install the required Python libraries using pip. Run the following commands in your terminal:

   ```bash
   pip install pygame
   pip install pillow
   pip install customtkinter
   pip install packaging
   ```

## Running the Application

1. Clone or download the project from the repository.

2. Navigate to the project directory.

3. Run the application using Python:

   ```bash
   python AudioQuizApp.py
   ```

## Usage

- **Start the Quiz**: Click on the 'Start Quiz' button to begin the quiz.

- **Play Audio Clips**: Click on the 'Play Clip' buttons to listen to the audio clips.

- **Submit Answer**: After selecting an audio clip, click 'Submit Answer' to check if your selection is correct.

- **Add Questions**: To add a new question, click on 'Add A Question' and fill in the details of the new quiz question. You can specify the title, audio clips, the correct answer, and optionally an album cover path.

- **Navigating Questions**: The application automatically moves to the next question after a correct answer. The quiz ends when all questions have been answered.

## Adding Questions Manually

You can add questions manually by editing the `questions.json` file. Each question should follow this format:

```json
{
  "title": "Song Title",
  "clips": ["path/to/clip1.mp3", "path/to/clip2.mp3", "path/to/clip3.mp3"],
  "correct": 0,
  "cover": "path/to/album_cover.jpg"
}
```

- `title`: The title of the song or question.
- `clips`: An array of paths to the audio clips.
- `correct`: The index (0, 1, or 2) of the correct audio clip.
- `cover`: (Optional) Path to an image file for the album cover.
