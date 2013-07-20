public
======

Programming for the internet.

shannon.py
---

This script approximates a passage of text. First, a frequency is calculated for all symbols (e.g. A-Z) in the source
text. Then symbols are independently chosen, with these probabilities, to generate a sequence of text. 


Here is an example from The Old Man and the Sea:

    lunae ehta dhdkrkeich d,erdaosh nu,h     y  amgh ronttesdwcr an  m oi cwh hhim eaiundlys  riy  f  eu
    
Which is better than choosing characters with equal probability:
  
    ;fklr,o.flbuouv;jgdtppqdpa!elv?-?eqskfpbahx?da,ozljjrlvhw.pvhfkk.doykk:?n.n,nkylyu?arkiaobtk?zel,?fx
    
    
    
Symbols can be selected with a probability that depends on the preceeding character:

    u haknd s. fthighoulld me the a he oucksaicok fislowil tild fabe h har. jusove s on oug, bll sh p f
    
Or the two preceeding characters:

    f then and now longs. it she dred theat not ther oad mas th alt. he fish sucky yon then ish quier a 

Or three:

     a pig wide. i will of the coulder to went coils of thought. i preating strippily, then he when me a
     
This is an approximated passage of The Old Man and the Sea where `n = 7`:

    lie down in the old mans hands in the pulls like the clouds over the old man, he thought. it is a
    sin to its perils and back to shifting-boats would see the starlight shut. he rested on the greener
    from an old fish together and the fishs head clear. then when he knew that half feet and that hard
    down a marlin. can i offer you at the clouds and you enjoyed kills everything now for him. now with
    flour sardines. the old man could see the current.
