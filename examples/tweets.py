from akeno import AkenoClient

akeno = AkenoClient("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


async def method():
    await akeno.fetch_tweet(00000000000000000000000)
    await akeno.get_tweet(0000000000000000000000000)
    await akeno.getch_tweet(00000000000000000000000)
    await akeno.fetch_tweets(
        0000000000000000000000,
        0000000000000000000000,
        0000000000000000000000
        )
    await akeno.like_tweet(00000000000, 00000000000)
    await akeno.unlike_tweet(00000000000, 000000000)
