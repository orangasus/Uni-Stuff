import donkeydefs
import donkeyinterface
import donkeylogic


def main():
    donkeydata = donkeylogic.init()

    while True:
        donkeyinterface.show_state(donkeydata)
        choice = donkeyinterface.prompt_choice(donkeydata)

        if choice == donkeydefs.QUIT:
            break
        elif choice == donkeydefs.FEED:
            donkeylogic.work(donkeydata)
        elif choice == donkeydefs.TICKLE:
            donkeylogic.tickle(donkeydata)
        elif choice == donkeydefs.WORK:
            donkeylogic.work(donkeydata)
        elif choice == donkeydefs.RESET:
            donkeydata = donkeylogic.init()


if __name__ == "__main__":
    main()
