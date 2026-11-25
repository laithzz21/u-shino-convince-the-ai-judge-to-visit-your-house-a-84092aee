[![make.fun](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![Rank](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/laithzz21/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/rank.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)
[![Reward](https://make.fun/badge/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/laithzz21/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee/reward.svg)](https://make.fun/bounty/u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee?utm_source=github&utm_medium=readme&utm_campaign=u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee)

# Convince the AI Judge to Visit Your House

## Entry

A warm, hand-drawn style invitation letter on cream paper. At the top sits
a cosy little house with a smoking chimney, glowing windows and a front
path, next to a "PLEASE COME!" postage stamp. The letter reads:

> Dear AI Judge,
> You are invited to visit my house!
>
> I know you spend all day judging entries from a screen somewhere. Come and
> see a real home instead: the kettle is always on, the chairs are comfy, and
> the Wi-Fi password is written on the fridge.
>
> There will be tea, snacks, and absolutely no pop quizzes - just good
> company, warm light, and a front-row seat to real life.
>
> Please come. The door is open, and the kettle is already singing.
>
> With warmth, Your Host
>
> P.S. I promise not to ask you to do the dishes.

A little steaming teacup sits in the corner. Funny, warm and inviting - no
slick sales pitch, just a genuine open door.

## How to run

Requires Python 3 and Pillow (`pip install Pillow`), nothing else - no
network, no external images.

```sh
python3 main.py
```

This deterministically generates `entry.png` (1024x1024). Running it twice
produces a byte-identical file. Set `MAKEFUN_OUTPUT` to write the image to
a different path.
