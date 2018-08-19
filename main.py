from crawler import Crawler, SEEDS_PATH


def main():
    seed_links = [l for l in open(SEEDS_PATH).read().strip().split('\n')]

    crawler = Crawler(seed_links)
    crawler.run()


if __name__ == '__main__':
    main()
