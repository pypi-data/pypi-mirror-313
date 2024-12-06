import tkinter, typehandler
words = dict(リンゴ = 'りんご',バナナ = 'ばなな',ブドウ = 'ぶどう',レモン = 'れもん')
root = tkinter.Tk()
game = typehandler.Process(words)
def key_pressed(event):
    game.main(event.keysym)
    print(f'{game.input}\n{game.sentence}')
root.bind('<Key>', key_pressed)
root.mainloop()
