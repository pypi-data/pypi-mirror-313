from qdrant_client.conversions.common_types import ScoredPoint
hits = [
    ScoredPoint(
        id=2215,
        version=34,
        score=0.9138969,
        payload={
            'nid': None, 
            'relative_url': None, 
            'seq_num': 38, 
            'source': 'loop_q_and_a_w_ref_text_meta.jsonl', 
            'text': 'Spørgsmål:\nHvem har ansvaret for medicinændringer, når borgeren selv adm. medicin? Den bliver rød i vores system, fordi borgeren jo er koblet på FMK. Men vi kommer kun i hjemmet hv.6.uge. til inj.  \n\nSvar:\n<p>Du må som sundhedsperson ikke administrere medicin, hvis medicinkortstatus er rød. Derfor er du nødt til at forholde dig til den samlede medicinering. Ændringen kan jo også dreje sig om det præparat, I administrerer.</p><p>Du er ansvarlig for at Ordinationsoversigten er opdateret. Ændringer, som vedrører medicin borger selv administrerer er en sag mellem borgeren og dennes læge</p>', 
            'title': 'Hvem har ansvaret for medicinændringer, når borgeren selv adm. medicin? Den bliver rød i vores system, fordi borgeren jo er koblet på FMK. Men vi kommer kun i hjemmet hv.6.uge. til inj.  '
        }, 
        vector=None, 
        shard_key=None
    ),
    ScoredPoint(
        id=2696, 
        version=42, 
        score=0.87595093, 
        payload={
            'nid': None, 
            'relative_url': None, 
            'seq_num': 509, 
            'source': 'loop_q_and_a_w_ref_text_meta.jsonl', 
            'text': 'Spørgsmål:\nHvis der sker en ændring i dosispk medicin f.eks e.l. opstarter blodtryksmedicin, men kommer det direkte i dosispk medicin. \nHvem har ansvaret for denne ændring? \nHvem har ansvaret for at en ny helbredstilstand bliver åbnet? \nEfter man fjernede ydelsen - modtag dosipk medicin er der ingen, der har det samme øje for ændringer, da det er mellem læge - patient - apotek. Står der i nogen instrukser, at når FMK er rød, at jeg så også har ansvaret for at opdatere helbredstilstand?\nHvordan i praksis vises denne tid til dokumentation?\n\nSvar:\nHar man kendskab til ændringer i en tilstand, så er man også forpligtiget til at handle på det.\n\nNår man har set en rød markering i FMK, anvendes ydelsen dosisdispensering. Det vil sige, der er ændringer, og behov for at sikre sig, at dosisposen er korrekt, og at medicinskemaet bliver ajourført.\nYdelsen kan ikke anvendes til modtage kontrol, da der kun ved rød markering i FMK er behov for kontrol af det dosispakkede medicin.', 
            'title': 'Ansvar, dosispk og helbredstilstande'
        }, 
        vector=None, 
        shard_key=None
    ), 
    ScoredPoint(
        id=884, 
        version=13, 
        score=0.8736099, 
        payload={
            'nid': 4489, 
            'relative_url': '/selvhaandtering-delvis-selvhaandtering-og-ingen-selvhaandtering-af-medicin', 
            'seq_num': 245, 
            'source': 'loop_documents_w_meta.json', 
            'text': 'Selvhåndtering, delvis selvhåndtering og ingen selvhåndtering af medicin\n<p>Defenitioner:</p>\n<ul>\n<li>Selvhåndtering, hvor borger selv dispenserer og indtager medicin (både fast og pn-medicin).</li>\n<li>Delvis selvhåndtering, hvis sundhedsperson eller apotek har ansvar for dispensering i dispenseringsæske eller dispensering i dosispose. Borgeren indtager selv medicinen.</li>\n<li>Ingen selvhåndtering, hvor sundhedspersonale eller apotek har ansvaret for, at dispensering i dispenseringsæske eller dispensering i dosispose, samt ansvar for, at borger støttes til at indtage medicinen.</li>\n</ul>\n<p>Selvhåndtering og delvis selvhåndtering af medicinen kan aftales i forhold til ét eller flere lægemidler. Dermed kan en borger i princippet være selvhåndterende på et lægemiddel og delvis på andre. Lægemidler som borgeren eller hospitalet administrerer skal overføres til "Ordinationsoversigten". Ved overførsel kan vælges \'Borger eller pårørende\' eller `eksternt sundhedsfagligt personale´ i feltet "Administreres af".</p>\n<p>Der er brug for løbende at revurdere, om borgeren har mere eller mindre brug for støtte til medicinhåndteringen. Denne vurdering skal foregå i samarbejde mellem borger, borgers egen læge, kontaktperson og forløbsansvarlige/SSA/spl. Der lægges i vurderingen vægt på, om borger kan:</p>\n<ul>\n<li>forstå ordinationen, herunder at handelsnavnet kan skifte</li>\n<li>forstå nødvendigheden af at tage medicin</li>\n<li>håndtere medicinen, uanset styrke og forstå, at dosis kan variere over tid</li>\n<li>tage medicinen rettidigt</li>\n<li>bestille medicin</li>\n<li>opbevare og bortskaffer medicinen korrekt</li>', 
            'title': 'Selvhåndtering, delvis selvhåndtering og ingen selvhåndtering af medicin'
        }, 
        vector=None, 
        shard_key=None
    )
]

expected_output = """<< Start af KONTEKST sektion >>

Uddrag nr 1:
> Spørgsmål:
> Hvem har ansvaret for medicinændringer, når borgeren selv adm. medicin? Den bliver rød i vores system, fordi borgeren jo er koblet på FMK. Men vi kommer kun i hjemmet hv.6.uge. til inj.  
> 
> Svar:
> <p>Du må som sundhedsperson ikke administrere medicin, hvis medicinkortstatus er rød. Derfor er du nødt til at forholde dig til den samlede medicinering. Ændringen kan jo også dreje sig om det præparat, I administrerer.</p><p>Du er ansvarlig for at Ordinationsoversigten er opdateret. Ændringer, som vedrører medicin borger selv administrerer er en sag mellem borgeren og dennes læge</p>
[Ref #1, {URL:<None>}]

Uddrag nr 2:
> Spørgsmål:
> Hvis der sker en ændring i dosispk medicin f.eks e.l. opstarter blodtryksmedicin, men kommer det direkte i dosispk medicin. 
> Hvem har ansvaret for denne ændring? 
> Hvem har ansvaret for at en ny helbredstilstand bliver åbnet? 
> Efter man fjernede ydelsen - modtag dosipk medicin er der ingen, der har det samme øje for ændringer, da det er mellem læge - patient - apotek. Står der i nogen instrukser, at når FMK er rød, at jeg så også har ansvaret for at opdatere helbredstilstand?
> Hvordan i praksis vises denne tid til dokumentation?
> 
> Svar:
> Har man kendskab til ændringer i en tilstand, så er man også forpligtiget til at handle på det.
> 
> Når man har set en rød markering i FMK, anvendes ydelsen dosisdispensering. Det vil sige, der er ændringer, og behov for at sikre sig, at dosisposen er korrekt, og at medicinskemaet bliver ajourført.
> Ydelsen kan ikke anvendes til modtage kontrol, da der kun ved rød markering i FMK er behov for kontrol af det dosispakkede medicin.
[Ref #2, {URL:<None>}]

Uddrag nr 3:
> Selvhåndtering, delvis selvhåndtering og ingen selvhåndtering af medicin
> <p>Defenitioner:</p>
> <ul>
> <li>Selvhåndtering, hvor borger selv dispenserer og indtager medicin (både fast og pn-medicin).</li>
> <li>Delvis selvhåndtering, hvis sundhedsperson eller apotek har ansvar for dispensering i dispenseringsæske eller dispensering i dosispose. Borgeren indtager selv medicinen.</li>
> <li>Ingen selvhåndtering, hvor sundhedspersonale eller apotek har ansvaret for, at dispensering i dispenseringsæske eller dispensering i dosispose, samt ansvar for, at borger støttes til at indtage medicinen.</li>
> </ul>
> <p>Selvhåndtering og delvis selvhåndtering af medicinen kan aftales i forhold til ét eller flere lægemidler. Dermed kan en borger i princippet være selvhåndterende på et lægemiddel og delvis på andre. Lægemidler som borgeren eller hospitalet administrerer skal overføres til "Ordinationsoversigten". Ved overførsel kan vælges 'Borger eller pårørende' eller \`eksternt sundhedsfagligt personale´ i feltet "Administreres af".</p>
> <p>Der er brug for løbende at revurdere, om borgeren har mere eller mindre brug for støtte til medicinhåndteringen. Denne vurdering skal foregå i samarbejde mellem borger, borgers egen læge, kontaktperson og forløbsansvarlige/SSA/spl. Der lægges i vurderingen vægt på, om borger kan:</p>
> <ul>
> <li>forstå ordinationen, herunder at handelsnavnet kan skifte</li>
> <li>forstå nødvendigheden af at tage medicin</li>
> <li>håndtere medicinen, uanset styrke og forstå, at dosis kan variere over tid</li>
> <li>tage medicinen rettidigt</li>
> <li>bestille medicin</li>
> <li>opbevare og bortskaffer medicinen korrekt</li>
[Ref #3, /selvhaandtering-delvis-selvhaandtering-og-ingen-selvhaandtering-af-medicin]

<< Slut på KONTEKST sektion >>"""