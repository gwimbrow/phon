#!/usr/bin/env python
import sys,random
consonants={'101':'160','102':'142','103':'164','104':'144','105':'372','106':'343','107':'143','108':'351','109':'153','110':'147','111':'161','112':'345','113':'120','114':'155','115':'115','116':'156','117':'357','118':'361','119':'116','120':'360','121':'340','122':'162','123':'366','124':'122','125':'363','126':'106','127':'102','128':'146','129':'166','130':'124','131':'104','132':'163','133':'172','134':'123','135':'132','136':'371','137':'374','138':'347','139':'112','140':'170','141':'107','142':'130','143':'113','144':'350','145':'121','146':'150','147':'110','148':'354','149':'320','150':'126','151':'364','152':'365','153':'152','154':'356','155':'154','156':'355','157':'114','158':'317','170':'167'}
vowels={'301':'151','302':'145','303':'105','304':'141','305':'101','306':'117','307':'157','308':'165','309':'171','310':'370','311':'367','312':'327','313':'066','314':'062','315':'067','316':'127','317':'061','318':'060','319':'111','320':'131','321':'125','322':'100','323':'070','324':'065','325':'346','326':'063','395':'306','397':'071'}
with open(sys.argv[1]) as source: verse=map(lambda x:x.rstrip().split(' '),['.'+s for s in source.readlines()])
morphemes=[m[0] for m in list(enumerate(' '.join([' '.join(v) for v in verse]).split(' '),start=1)) if '.' in m[1]]
verse=[map(lambda x:x.replace('.',''),v) for v in verse]
numbers=[[o[i:i+3] for i in range(0,len(o),3)] for o in ' '.join([' '.join(s) for s in verse]).split(' ')]
syllables=list(enumerate([''.join(o) for o in numbers],start=1))
lit=[]
while len(syllables)>0:
  phonemes='\\null\\vfill'
  n=[]
  count=1
  match=False
  for ln in range(len(verse)):
    phonemes+='\centerline{'
    phon=''
    for sn in range(len(verse[ln])):
      if count in morphemes: phonemes+='\enskip'
      elif sn>0 and not phonemes.endswith('\enskip'): phonemes+="\ipa\char'056"
      syll=[]
      source=[verse[ln][sn][i:i+3] for i in range(0,len(verse[ln][sn]),3)]
      while len(syll)<len(source):
        if source[len(syll)] in consonants.keys():
          if len(syll)==0: pre=[ph[0] for ph in numbers if ph[0] in consonants.keys()]
          elif phon!='': pre=[ph[ph.index(phon)+1] for ph in numbers if phon in ph and len(ph)-1>ph.index(phon) and ph[ph.index(phon)+1] in consonants.keys()] if len(syll)+1!=len(source) else [ph[ph.index(phon)+1] for ph in numbers if phon in ph and len(ph)-1==ph.index(phon)+1 and ph[ph.index(phon)+1] in consonants.keys()]
        elif source[len(syll)] in vowels.keys():
          if len(syll)==0: pre=[ph[0] for ph in numbers if ph[0] in vowels.keys()]
          elif phon!='': pre=[ph[ph.index(phon)+1] for ph in numbers if phon in ph and len(ph)-1>ph.index(phon) and ph[ph.index(phon)+1] in vowels.keys()] if len(syll)+1!=len(source) else [ph[ph.index(phon)+1] for ph in numbers if phon in ph and len(ph)-1==ph.index(phon)+1 and ph[ph.index(phon)+1] in vowels.keys()]
        try:
          phon=random.choice([p for p in pre if p!=phon])
          syll.append(phon)
        except IndexError: syll=[]
      sb=''.join(syll)
      if sb not in [s[1] for s in syllables] and sb in [''.join(o) for o in numbers] or sb in [s[1] for s in syllables] and len([s for s in syllables if s[0]==count and s[1]==sb])==0 or sb in [s[1] for s in syllables] and match==True:
        sb=''
        if phonemes.endswith("\ipa\char'056"): phonemes=phonemes[:len(phonemes)-13]+'\enskip'
      if sb in [s[1] for s in syllables] and match==False: phonemes+='\pdfcolorstack\match push{1 0 0 rg}'
      for s in syll: phonemes+="\ipa\char'"+dict(consonants.items()+vowels.items())[s] if sb!='' else '\enskip'
      if sb in [s[1] for s in syllables] and match==False:
        phonemes+='\pdfcolorstack\match pop{}'
        n.append(syllables.pop(syllables.index((count,sb)))[0])
        match=True
      count+=1
    phonemes+='}\\bigskip'
  if match==True: lit.append(phonemes+'\\vfill\\footline={\hfill\\tenrm\it '+','.join(map(str,n))+' / '+str(len([''.join(o) for o in numbers]))+'}\eject')
with open(sys.argv[1]+'.tex','w') as temp: temp.write('\pdfcompresslevel=0\chardef\match=\pdfcolorstackinit page direct{0 g}\\nopagenumbers\\font\ipa=tipa17\pdfpagewidth 216 true mm\pdfpageheight 356 true mm\pdfhorigin 25.4 true mm\pdfvorigin 25.4 true mm\hsize 165.2 true mm\\vsize 305.2 true mm\n'+'\n'.join(lit)+'\\bye')