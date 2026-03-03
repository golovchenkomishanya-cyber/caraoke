from pygame import *
import sounddevice as sd
import scipy.io.wavfile as wav

init()

window = display.set_mode((500,500))
display.set_caption("TEST")
clk = time.Clock()
fps = 60
running = True

f = font.SysFont("Arial",30)
title_font = font.SysFont("Arial", 40)
title_text = title_font.render("Запис твого голосу", 1, (255,255,255))

class Button:
    def __init__(self, x, y, w, h, text):
        self.text = text
        self.text_img = f.render(self.text, 1, (0,0,0))
        self.rect = Rect(x, y, w, h)
        self.recording = False
        self.data = None
        self.start_time = 0

    def click(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if not self.recording:
                    self.recording = True
                    self.text = "Зупинити"
                    self.text_img = f.render(self.text, 1, (0,0,0))
                    self.start_time = time.get_ticks()
                    self.data = sd.rec(int(5 * 44100), samplerate=44100, channels=1)
                else:
                    sd.stop()
                    end_time = time.get_ticks()
                    duration_ms = end_time - self.start_time
                    samples_recorded = int((duration_ms / 1000) * 44100)
                    trimmed_data = self.data[:samples_recorded]
                    wav.write("output.wav", 44100, trimmed_data)
                    self.recording = False
                    self.text = "Почати"
                    self.text_img = f.render(self.text, 1, (0,0,0))

    def draw(self, win):
        draw.rect(win, (0,0,0), self.rect, 2)
        win.blit(self.text_img, (self.rect.x + 10, self.rect.y + 10))

BTN = Button(175,250,150,50,"Почати")

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        BTN.click(e)

    window.fill((10, 60, 30))
    window.blit(title_text, (70, 80))
    BTN.draw(window)
    display.update()
    clk.tick(fps)