<div align="center">
  <br />
  <p>
    <a href="https://discord.gg/GTJtFGUNV5"><img src="https://cdn.donmai.us/original/65/bd/__modeus_helltaker_drawn_by_kiyovero__65bd0b99d080bceb39fff3f4de7cc586.png" width="146" height="200"/></a>
  </p>
  <br />
</div>
sara is both a SFW and NSFW Wrapper, there's hentais for you perverts to use, however do understand that I'm the only one working on this, and I hand pick images to add, so you may get repeated images! Use it for your Discord Bot, your Self Made Console Waifu, or whatever it is :3

## NOTE: This Readme.md is from the [Offical Repository](https://gitlab.com/weeb-squad/akaneko/)

## Changelogs
### v0.1
- new api

### v1.1
- new commands
- new categories

### v1.6
- new funcion
- connect nhentai get cover image

### v1.1.8
- function repair
- readme change

## Example(s)
**Python:**
```python
import sara

def function_name():
  # Get SFW Neko Images, uwu #
  print("SFW Neko: " + sara.sfw.neko())

  # Get other NSFW Images#
  print("BDSM: " + sara.nsfw.bdsm())
  print("Maid: " + sara.nsfw.maid())
  print("Hentai: " + sara.nsfw.hentai())

# Call Your Function!
function_name()

```


## SFW Function(s)
Example:
```python
sara.module.function() # Format
sara.sfw.foxgirl()     # Awoo!~ Another example!
sara.sfw.neko()        # Meow! An Example!
```
Function | Description
---|---
neko | SFW Neko Girls (Cat Girls) - Purrfectly cute!
foxgirl | SFW Fox Girls - For when you're feeling foxy
sad | For when your waifu leaves you on read
angry | When someone says anime is just for kids
work | Anime characters grinding harder than you
yandere | For those who like their love... intense
wink | When you make an "I watch it for the plot" joke
vomit | When you realize your waifu isn't real
teehee | For those moments when you're being a little naughty
pout | When senpai doesn't notice you
laugh | When you tell your friends you'll stop watching anime
dance | Shake what your waifu gave ya!
cry | For when the season finale hits different
bored | When you're waiting for the next episode to drop
blush | When senpai finally notices you
run | When your parents walk in during an "intense" scene

## rolplay sfw
Function | Description
---|---
baka | For when your friend says they prefer dubs
kiss | A smooch so sweet it'll give you cavities
kill | When someone spoils the latest episode
sfwspank | A gentle reminder to behave (keep it clean, folks!)
punch | For when words just aren't enough
poke | When you need attention but are too shy to ask

## NSFW Function(s)
Function | Description
---|---
ass | I know you like anime ass~ uwu
bdsm | If you don't know what it is, search it up
blowjob | Basically an image of a girl sucking on a sharp blade!
boobs | boobs ~<3
cum | Basically sticky white stuff that is usually milked from sharpies.
doujin | Sends a random doujin page imageURL!
feet | So you like smelly feet huh?
femdom | Female Domination?
foxgirl | Girl's that are wannabe foxes, yes
gifs | Basically an animated image, so yes :3
glasses | Girls that wear glasses, uwu~
hentai | Sends a random vanilla hentai imageURL~
ahegao | Sends a random ahegao image ~
netorare | Wow, I won't even question your fetishes.
maid | Maids, Maid Uniforms, etc, you know what maids are :3
masturbation | Solo Queue in CSGO!
orgy | Group Lewd Acts
panties | I mean... just why? You like underwear?
pussy | The genitals of a female, or a cat, you give the meaning.
school | School Uniforms!~ Yatta~!
succubus | Spooky Succubus, oh I'm so scared~ Totally don't suck me~
tentacles | I'm sorry but, why do they look like intestines?
thighs | The top part of your legs, very hot, isn't it?
uglyBastard | The one thing most of us can all agree to hate :)
uniform |Military, Konbini, Work, Nurse Uniforms, etc!~ Sexy~
yuri | Girls on Girls, and Girl's only!<3
zettaiRyouiki | That one part of the flesh being squeeze in thigh-highs~<3

## rolplayNsfw Function(s)
Function | Description
---|---
rolplayNsfw.fuck | When "Netflix and chill" gets serious
rolplayNsfw.anal | For those who like to explore the back catalog
rolplayNsfw.happyend | Not your typical fairy tale ending
rolplayNsfw.kuni | Giving a new meaning to "eating out"
rolplayNsfw.spank | For those who've been very, very naughty
rolplayNsfw.suck | More than just a lollipop, if you know what I mean
rolpayNsfw.feetjob | For those with sole-ful desires


## wallpáper Function(s)
Function | Description
---|---
sara.sfw.mobileWallpapers() | Fetch a random SFW Wallpaper! (Mobile)
sara.sfw.wallpapers() | Fetch a random SFW Wallpaper! (Desktop)
sara.nsfw.mobileWallpapers() | Fetch a random NSFW Wallpaper! (Mobile)
sara.nsfw.wallpapers() | Fetch a random NSFW Wallpaper! (Desktop)



##
Discord Bot Example
```python
import discord # Import the module
import sara

from discord.ext import commands # get commands from discord.ext

client = commands.Bot(command_prefix='[PREFIX HERE]')

@client.event # the function decorator
async def on_ready(): # on Ready event
  print(f"Ready as {client.user}") # print the bot's tag when its ready

@client.command() # Make a isinstance for the command
async def neko(ctx): # Make the function and pass in `ctx` as the params
  print(sara.sfw.neko())

client.run("token") # token here

```

## Any Bugs? [Open a issue](https://github.com/EverGasterXd/sara_api/issues) or dm evergaster