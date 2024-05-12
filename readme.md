<style>
h1, h2
{
    color:white;
}

hr
{
    background-color:white;
}

h3
{
    color:lightgrey;
    font-style:italic;
}

</style>

<center> 
    <h1>Adatelmezés</h1>

<hr>

<h1>Projektet készítették</h1> 
<hr>
<h2><span style="font-style:italic">Adatgyűjtő</span><br> Kássa Gergő (HL347M)</h2>
<h2><span style="font-style:italic">Adatelemző</span><br> Benák Krisztián (YMCMI2)</h2>
<h2><span style="font-style:italic">Storyteller</span><br> Kássa Dávid (L123PZ)</h2>

<hr>

<h1> Fileok feladata</h1>

<hr>

<h2>main.py</h2>
<h3>Ebben hívjuk meg a függvényeket,
illetve itt hozunk létre plotokat az adatok ábrázolásához</h3>
<hr>

<h2>functions_for_animes.py</h2>
<h3>
A projekt feladatait kiszervezzük hívható függvényekként.<br><br>
Ebben a fileban például implementáltunk a következőket: <br><br>
Adatok beolvasását/írását json fileból/ba<br><br>
API-ból az adatok lekérdezéséhez logikát<br><br>
Dataframe létrehozása.<br><br> És még sok egyéb ilyen függvény található a fileban, amik segítik a feladatok elvégzését.
</h3>
<hr>

<h2>anime_info.py</h2>
<h3>
Ez egy modell az Animékhez, amiben tároljuk az animék azonosítóját, neveit, értékeléséeit, megjelenési dátumát, híreit, műfajait, témáit és olyan animék azonosítóját, amik kapcsolódnak az adott animéhez. 
</h3>
<hr>

<h2>animeinfodata.json</h2>
<h3>
Ebben a fileban tároljuk az API-ból kapott adatokat. Ha nem lennének tárolva az adatok, akkor minden futás előtt körülbelül 5 percet kellene várni, amég az API 50-es batchekben átadja nekünk az adatokat.
</h3>
<hr>


















</center>


