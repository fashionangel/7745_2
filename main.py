from seven_parc import Parser
import time



def main():
    parser = Parser('https://7745.by/catalog/obogrevateli')

    parser.accept_cookie()
    time.sleep(5)

    try:
        parser.electro_choice()
        time.sleep(1.5)

        parser.power()
        time.sleep(2)

        parser.power_second()
        time.sleep(1)

        parser.mange()
        time.sleep(2.5)

        parser.show_product()
        time.sleep(1)

        all_links = parser.get_all_links_on_page()
        for link in all_links:
            print(link)

        parser.get_info()
        print(parser.info_list)

        parser.creating_csv_file()
    except Exception:
        parser.switchOptions()
        main()



if __name__ == "__main__":
    main()