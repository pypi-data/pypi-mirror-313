import pygame, sys
from typehandler import Process

pygame.init()
screen = pygame.display.set_mode((600, 500))
pygame.display.set_caption('example')

font =  pygame.font.SysFont("MSP Gothic", 32)

def vocalize(a):
    #音声を再生する
    pygame.mixer.init(frequency=44100)
    pygame.mixer.set_num_channels(32)
    sound_key = pygame.mixer.Sound(a)
    sound_key.play()

words = dict(リンゴ = 'りんご',
             ブドウ = 'ぶどう',
             レモン = 'れもん',
             バナナ = 'ばなな',
             )

def main():
    clock = pygame.time.Clock()
    process = Process(words)
    while True:
        process.update_show_roman()
        screen.fill((255, 255, 255))
        text_roman = font.render(process.show_roman, True, (192, 192, 192))
        text_input = font.render(process.input, True, (0, 0, 0))
        text_sentence = font.render(process.sentence, True, (0, 0, 0))
        pygame.draw.line(screen, (0, 128, 255), (0, 50), (600, 50), 5)    #青い線を描画
        pygame.draw.line(screen, (255, 128, 0), (0, 150), (600, 150), 5)    #オレンジの線を描画
        screen.blit(text_roman, (30,60))
        screen.blit(text_input, (30,60))
        screen.blit(text_sentence, (30, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                correct_input = process.check_correct_input(pygame.key.name(event.key))    #ミスタイプを判定
                if correct_input:
                    vocalize('input.ogg')
                    chunk_conpleted = process.check_chunk_completion()    #文の打ち終わりを判定
                    if chunk_conpleted:
                        sentence_completed = process.check_sentence_completion()
                        if sentence_completed:
                            vocalize('next.mp3')
                            process.set_new_sentence()    #新しい文を用意
                else:
                    vocalize('miss.ogg')
        pygame.display.update()
        clock.tick(50)

if __name__ == '__main__':
    main()
