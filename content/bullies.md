Title: When bullies kill by mistake
Date: 2017-07-17 10:20
Category: Data Science
Tags: mafia, web-scrap, beautifulsoup python

I am Italian. Although I left Italy almost ten years ago, I still feel very attached to my country, my people and my culture. Unfortunately, Italy is not pizza and mandolino. In the last century, Italy has been tormented by a series of unfortunate events: fascism, corruption in the public sector, the financial crisis, Berlusconi. But there is one phenomenon (a combination of all of above) which still rules them all.  It has been spreading and rooting like a cancer for 150 years: mafia.

I do not want to get into why mafia exists, why mafia is everywhere but you can only see it in the south of Italy, why it is embedded in Italian politics or why it seems so hard to eradicate. To me, mafia is just of bunch of ignorant bullies who pretend to be above the law. These people will mask their involvement in money laundering or drug trafficking with words such as “honour”, “family” or “protection” (by themselves).

What I mostly care about is that mafia kills innocent people. If you are unlucky enough to be in the middle of a gun-fight between gangs, you are doomed. The reason for these killings vary, but can be split into two categories: 1) killed because at the wrong place at the wrong time; 2) killed because the victim stood up for his/her rights (e.g., by reporting racket to authorities). Gang related gun-fights happen under the sunlight, in city centres, in squares full of human beings. And it happens just a few kilometres from my hometown.

I wanted to have a feeling of how many innocent people died because of these stupid fights between bullies. So, I scraped data from three websites: vittimedimafia.it, libera.it and peppinoimpastato.com . [Peppino Impastato](https://en.wikipedia.org/wiki/Giuseppe_Impastato) was himself a man who got killed because he dared to openly oppose the mafia in his hometown in Sicily.

The source-code to scrap the data and plot the graphs below can be found [here](https://github.com/vincepota/mafia-victims). The graph below shows the cumulative mafia death tool since the first recorded case in 1861. Cumulative means that at every point in time on the x-axis, the death tool on the y-axis is the successive additions of the victims from previous years.


![I am text]({filename}/images/mafia.png)

The three datasets show the same trend. Libera.it seems to be more complete compared to the other two sources. The message is clear: between 800 and 1000 innocent people were killed by mafia in the last century. A more accurate number is probably over a thousand (1126 as in March 2017). Death tool started rising in the 80’s, reaching 64 in 1983 and 83 in 1989, the worst year on record. These were years of political and social turmoil in Italy when many more people were killed in terror attacks not related to mafia. In the 90’s and 2000’s deaths have been gradually decreasing and we now have an average of 3 innocent victims per year.

![I am text]({filename}/images/mafia_discrete.png)

How do we fix this? Jailing all these criminals today will not fix the problem. Kids and teenagers growing-up in an environment heavily colluded with the mafia will likely become criminals themselves. Not their fault. It is with prevention and education that we stop the kids of today growing up as mafia bosses. Local communities are doing their best and huge progresses have been made in the past years. There are people devoting (literally) their own lives to eradicate mafia from the Italian culture. These people are my heroes. They make me proud of being Italian.
