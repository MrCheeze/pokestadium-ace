# pokestadium-ace
Notes and code related to getting arbitrary code execution on Pokemon Stadium for the N64. For a demonstration payload, [see here](https://www.youtube.com/watch?v=Bb0v-VDsBkQ).

----

The key point of this exploit is that getting ACE in Stadium requires first getting ACE in Pokemon R/B/Y (or a similarly powerful memory manipulation glitch), so that the Game Boy save can be manipulated at will. However, since it is possible to play first-generation Pokemon games within Stadium at the GB Tower, it is still possible to do everything from within Stadium proper.

Two N64 controllers with two Transfer Paks and two Game Boy games are required to enter Pokemon Stadium's trading system, where the exploit lies. Both games must also have a Pokedex, and be saved in a Pokemon Center. However, only the second game's save file needs to be glitched at all.

----

## Exploit details

When using the trade machine, each game's Pokemon boxes are converted from R/B/Y's format to Stadium's format, and placed at the following locations in memory.

    80129D68 - game 1 party
    8012A404 - game 1 box 1
    8012AAA0 - game 1 box 2
    8012B13C - game 1 box 3
    8012B7D8 - game 1 box 4
    8012BE74 - game 1 box 5
    8012C510 - game 1 box 6
    8012CBAC - game 1 box 7
    8012D248 - game 1 box 8
    8012D8E4 - game 1 box 9
    8012DF80 - game 1 box 10
    8012E61C - game 1 box 11
    8012ECB8 - game 1 box 12

    80130000 - game 2 party
    8013069C - game 2 box 1
    80130D38 - game 2 box 2
    801313D4 - game 2 box 3
    80131A70 - game 2 box 4
    8013210C - game 2 box 5
    801327A8 - game 2 box 6
    80132E44 - game 2 box 7
    801334E0 - game 2 box 8
    80133B7C - game 2 box 9
    80134218 - game 2 box 10
    801348B4 - game 2 box 11
    80134F50 - game 2 box 12

Each box contains a half-word for the number of Pokemon in the box, a pointer to the previous box, and a pointer to the next box, followed by 20 Pokemon structs. Each Pokemon struct is 0x54 bytes long and has the following format:

    u8 species
    u8 gen_1_index_number
    u16 current_hp

    u8 pc_level
    u8 status
    u8 type1
    u8 type2

    u8 held_item
    u8 move1
    u8 move2
    u8 move3

    u8 move4
    u8 unknown_but_usually_89
    u16 ot_id

    u32 exp

    u16 hp_ev
    u16 attack_ev

    u16 defense_ev
    u16 speed_ev

    u16 special_ev
    u16 IVs

    u8 pp1 (current/max)
    u8 pp2 (current/max)
    u8 pp3 (current/max)
    u8 pp4 (current/max)

    u8 level
    u8 unknown_but_usually_00
    u16 max_hp

    u16 attack
    u16 defense

    u16 speed
    u16 special

    char[11] nickname
    char[11] original_trainer
    char[11] original_trainer_gb_encoding

    u8 unknown_but_usually_2A
    u16 unknown_but_usually_0000

If the gameboy save says there is more than 20 Pokemon in a box, the buffer will overflow, overwriting whatever comes in memory after it. Nothing useful whatsoever happens from overflowing beyond Game 1 Box 12, but some interesting things are located after Game 2 Box 12. By far the most notable is 801356B0, a code pointer. If this pointer is nonzero, the game will automatically jump execution to wherever it points when on the "Choose the Game Paks for trading" screen. We can overwrite this pointer with any value we want by making the second gameboy game have 23 Pokemon in box 12. However, to prevent crashing, we must take care not to overwrite other variables nearby in memory - or rather, to overwrite them with the same value they had originally. To be specific, the pointer at 801356A8 must keep its current value of 80135830, and the halfword at 80135630 must remain zero (the latter requires us to actually place a 0x50 rather than a zero in the GB save file, due to the conversion from R/B/Y's encoding to ASCII).

As you would probably expect, we change the code pointer at 801356B0 to point to somewhere within the Game Boy save itself. Therefore it's necessary to mention where exactly the save files are copied into N64 memory. Note that if the main data states that the player has yet to ever change boxes, then the additional box data is never copied to memory.

GB Cart 1:
* copy from GB save file 2580-3540 to N64 ram 801E09E0-801E19A0 (first cart main data)
* copy from GB save file 4000-5A60 to N64 ram 801E19B0-801E3410 (first cart box 1-6)
* copy from GB save file 6000-7A60 to N64 ram 801E3410-801E4E70 (first cart box 7-12)
GB Cart 2:
* copy from GB save file 2580-3540 to N64 ram 801E4EA0-801E5E60 (second cart main data)
* copy from GB save file 4000-5A60 to N64 ram 801E5E70-801E78D0 (second cart box 1-6)
* copy from GB save file 6000-7A60 to N64 ram 801E78D0-801E9330 (second cart box 7-12)

Some documentation on RBY's save format can be found in the pokered disassembly project [here](https://github.com/pret/pokered/blob/master/sram.asm) and [here](https://github.com/pret/pokered/blob/master/wram.asm). Note that while storing payloads in the box data is convenient due to the considerable amount of space, one should take care to make sure that boxes other than #12 have no more than 12 Pokemon, to prevent accidentally causing *additional* buffer overflows.

The theoretical absolute maximum size of a payload - if data is stored in four GB saves rather than just one, and additional code is written to copy the entirety of all four saves to N64 RAM - is a little less than 128 KB.

----

## Failed efforts

To prevent duplicate effort, I should mention other seemingly-plausible candidates for ACE exploits that didn't work out. All three games in the Stadium series feature a built-in Game Boy emulator, and it seemed plausible that an exploit could exist in these emulators that allows us - given that we have an exploit to run arbitrary GB code - to "escape" the emulator and run arbitrary N64 code as well. However, after extensive reverse engineering work on Pokemon Stadium 2's GB tower, it appears to be the case that extensive error checking is done on the GB code, and no such exploit is possible. Consulting with other reverse engineers such as Zoinkity who have worked on the other two emulators confirms that the same is true for them.

Unlike Pokemon Stadium 1, Pokemon Stadium 0 (the Japanese-only first game) does not appear to have the trade machine we need to exploit it. Pokemon Stadium 2 has the machine, but does more thorough error-checking on the save files it loads, and is therefore useless for our purposes.

Well the trade machine is the only known exploitable machine in Stadium 1, it is not ruled out that the other lab machines have exploits of their own, however I was not personally able to find any such exploit. If one exists, it would reduce the number of Game Boy cartridges and Transfer Paks needed from 2 to 1.

----

## Other files

The following files are the ones I used while researching the game and testing this ACE exploit, and are included in case anyone finds them helpful:

* generate_save.py - Code used to generate the game boy save files used in my demonstration.
 * Red.sav - A completely ordinary save file, only necessary because trading Pokemon necessarily requires two Game Boy games.
 * Blue.sav - The savefile that contains both the trigger for the ACE, as well as the payload proper.
* rgba5551.py - A hastily thrown together script to convert images to the 16-bit texture format used in Pokemon Stadium, used in my demonstration payload.
 * cosmog.png, texture.png - Images used by my payload.
* stadium_notes.txt - My own notes taken while researching / reverse engineering the game. Comprehensibility not guaranteed.
 
