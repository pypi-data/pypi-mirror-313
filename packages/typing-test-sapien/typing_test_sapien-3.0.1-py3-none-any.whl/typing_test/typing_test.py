import time
import random
import getpass
import os

sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "The best time to plant a tree was years ago. The second best time is now.",
    "What you get by achieving your goals is not as important as what you become by achieving your goals.",
    "Believe you can, and you are halfway there.",
    "Do not wait for the perfect moment; take the moment and make it perfect.",
    "You cannot go back and change the beginning, but you can start where you are and change the ending.",
    "Every accomplishment starts with the decision to try.",
    "Hardships often prepare ordinary people for an extraordinary destiny.",
    "Your only limit is your mind.",
    "You are never too old to set another goal or to dream a new dream.",
    "It is not what happens to you but how you react to it that matters.",
    "The first email ever sent was by Ray Tomlinson in the early seventies.",
    "More than ninety percent of the world's currency exists only in digital form.",
    "The first website ever created is still online today.",
    "The first video uploaded to YouTube was titled 'Me at the zoo.'",
    "The QWERTY keyboard was designed to slow down typists to prevent typewriter jams.",
    "Ada Lovelace is considered the world's first computer programmer.",
    "The original name for Windows was Interface Manager.",
    "Five billion videos are watched on YouTube every day.",
    "There are countless bytes of data created every single moment.",
    "The first one-gigabyte hard drive weighed as much as a small car.",
    "The first manned moon landing was made by Apollo Eleven.",
    "The fall of the Berlin Wall marked the end of the Cold War.",
    "Julius Caesar was assassinated on the Ides of March.",
    "The Declaration of Independence was signed in the late eighteenth century.",
    "The Titanic sank after hitting an iceberg on a cold April night.",
    "Mahatma Gandhi led the Salt March to protest British rule in India.",
    "The first World War lasted for four long years.",
    "The Black Death changed the course of European history.",
    "Nelson Mandela became South Africa's first black president after years of struggle.",
    "The Great Fire of London destroyed much of the city but led to modernization.",
    "Water naturally exists in three states: solid, liquid, and gas.",
    "The speed of light is an unbreakable universal constant.",
    "Your DNA contains instructions unique to you and could stretch across the solar system.",
    "There are more atoms in a single glass of water than stars in the observable universe.",
    "A teaspoon of honey represents the life work of dozens of bees.",
    "The blue whale's heart is as large as a small car.",
    "The surface temperature of the sun is incredibly high, making it inhospitable for life.",
    "Bacteria outnumber human cells in your body.",
    "The Great Wall of China is visible from low Earth orbit.",
    "Harry Potter and the Philosopher's Stone brought magic into millions of lives.",
    "The Star Wars saga has captured the imaginations of generations.",
    "The Beatles revolutionized the music industry.",
    "The Marvel Cinematic Universe has become the highest-grossing film franchise.",
    "Friends, the TV sitcom, remains iconic even decades after its premiere.",
    "The Olympic Games are a global celebration of athletic excellence.",
    "The Mona Lisa by Leonardo da Vinci is a masterpiece of the Renaissance.",
    "The Game of Thrones series concluded with a highly debated ending.",
    "The Lord of the Rings trilogy showcased breathtaking landscapes and epic storytelling.",
    "The phrase 'May the Force be with you' is synonymous with Star Wars.",
    "A group of crows is known as a murder.",
    "Every man dies. Not every man really lives. Braveheart",
    "Oh, Captain! My Captain! Dead Poets Society",
    "My precious. The Lord of the Rings: The Two Towers",
    "You either die a hero, or you live long enough to see yourself become the villain. The Dark Knight",
    "The only way to do great work is to love what you do. Steve Jobs",
    "In the middle of every difficulty lies opportunity. Albert Einstein",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. Winston Churchill",
    "Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment. Buddha",
    "Happiness is not something ready-made. It comes from your own actions. Dalai Lama",
    "Life is what happens when you're busy making other plans. John Lennon",
    "To live is the rarest thing in the world. Most people exist, that is all. Oscar Wilde",
    "It always seems impossible until it is done. Nelson Mandela",
    "Do not go where the path may lead, go instead where there is no path and leave a trail. Ralph Waldo Emerson",
    "What lies behind us and what lies before us are tiny matters compared to what lies within us. Ralph Waldo Emerson",
    "Whether you think you can or you think you can’t, you’re right. Henry Ford",
    "The best way to predict the future is to create it. Peter Drucker",
    "The journey of a thousand miles begins with a single step. Lao Tzu",
    "The purpose of life is not to be happy. It is to be useful, to be honorable, to be compassionate, to have it make some difference that you have lived and lived well. Ralph Waldo Emerson",
    "The future belongs to those who believe in the beauty of their dreams. Eleanor Roosevelt",
    "You miss 100%\ of the shots you don’t take. Wayne Gretzky",
    "Don’t let yesterday take up too much of today. Will Rogers",
    "Perseverance is not a long race; it is many short races one after the other. Walter Elliot",
    "Do what you can, with what you have, where you are. Theodore Roosevelt",
    "You are never too old to set another goal or to dream a new dream. C.S. Lewis",
    "The only limit to our realization of tomorrow will be our doubts of today. Franklin D. Roosevelt",
    "Act as if what you do makes a difference. It does. William James",
    "Keep your face always toward the sunshine—and shadows will fall behind you. Walt Whitman",
    "Everything you’ve ever wanted is on the other side of fear. George Addair",
    "Dream big and dare to fail. Norman Vaughan",
    "I have not failed. I've just found 10,000 ways that won’t work. Thomas Edison",
    "Success is how high you bounce when you hit bottom. George S. Patton",
    "If opportunity doesn’t knock, build a door. Milton Berle",
    "It’s not whether you get knocked down, it’s whether you get up. Vince Lombardi",
    "Believe in yourself and all that you are. Christian D. Larson",
    "Success usually comes to those who are too busy to be looking for it. Henry David Thoreau",
    "The secret of getting ahead is getting started. Mark Twain",
    "Don’t watch the clock; do what it does. Keep going. Sam Levenson",
    "You must be the change you wish to see in the world. Mahatma Gandhi",
    "It’s never too late to be what you might have been. George Eliot",
    "The only person you are destined to become is the person you decide to be. Ralph Waldo Emerson",
    "He who has a why to live can bear almost any how. Friedrich Nietzsche",
    "What we achieve inwardly will change outer reality. Plutarch",
    "Courage doesn’t always roar. Sometimes courage is the quiet voice at the end of the day saying, 'I will try again tomorrow.' Mary Anne Radmacher",
    "Start where you are. Use what you have. Do what you can. Arthur Ashe",
    "You must do the things you think you cannot do. Eleanor Roosevelt",
    "Be yourself; everyone else is already taken. Oscar Wilde",
    "Strive not to be a success, but rather to be of value. Albert Einstein",
    "The best way out is always through. Robert Frost",
    "Do not wait to strike till the iron is hot; but make it hot by striking. William Butler Yeats",
    "You cannot cross the sea merely by standing and staring at the water. Rabindranath Tagore",
    "It takes as much energy to wish as it does to plan. Eleanor Roosevelt",
    "Life is short, and it is here to be lived. Kate Winslet"
    "It is never too late to be what you might have been. George Eliot",
    "What you do today can improve all your tomorrows. Ralph Marston",
    "Don’t let the fear of losing be greater than the excitement of winning. Robert Kiyosaki",
    "An unexamined life is not worth living. Socrates",
    "Do not fear failure but rather fear not trying. Roy T. Bennett",
    "Limit your 'always' and your 'nevers.' Amy Poehler",
    "Success is liking yourself, liking what you do, and liking how you do it. Maya Angelou",
    "Turn your wounds into wisdom. Oprah Winfrey",
    "Happiness is not by chance, but by choice. Jim Rohn",
    "Success is the sum of small efforts, repeated day in and day out. Robert Collier",
    "If you want to lift yourself up, lift up someone else. Booker T. Washington",
    "The only way to achieve the impossible is to believe it is possible. Charles Kingsleigh",
    "We know what we are, but know not what we may be. William Shakespeare",
    "Nothing is impossible, the word itself says, 'I’m possible!' Audrey Hepburn",
    "The mind is everything. What you think you become. Buddha",
    "The greatest wealth is to live content with little. Plato",
    "Do not follow where the path may lead. Go instead where there is no path and leave a trail. Ralph Waldo Emerson",
    "Dream as if you’ll live forever. Live as if you’ll die today. James Dean",
    "The best revenge is massive success. Frank Sinatra",
    "We are what we repeatedly do. Excellence, then, is not an act, but a habit. Aristotle",
    "You can’t use up creativity. The more you use, the more you have. Maya Angelou",
    "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful. Albert Schweitzer",
    "Challenges are what make life interesting, and overcoming them is what makes life meaningful. Joshua J. Marine",
    "The only impossible journey is the one you never begin. Tony Robbins",
    "Happiness depends upon ourselves. Aristotle",
    "Your time is limited, so don’t waste it living someone else’s life. Steve Jobs",
    "Be the change that you wish to see in the world. Mahatma Gandhi",
    "Fall seven times and stand up eight. Japanese Proverb",
    "Whatever you are, be a good one. Abraham Lincoln",
    "I can’t change the direction of the wind, but I can adjust my sails to always reach my destination. Jimmy Dean",
    "The Olympic Games originated in ancient Greece over 2,700 years ago.",
    "The FIFA World Cup is the most-watched sports event in the world.",
    "Basketball was invented in 1891 by Dr. James Naismith.",
    "Cricket is the second most popular sport in the world after soccer.",
    "The Wimbledon Championships is the oldest tennis tournament in the world.",
    "The Boston Marathon is the oldest annual marathon, first held in 1897.",
    "Baseball is known as America’s national pastime.",
    "Usain Bolt holds the world record for the 100-meter sprint.",
    "The first Super Bowl was played in 1967.",
    "Michael Jordan won six NBA championships with the Chicago Bulls.",
    "The Tour de France is the most prestigious cycling race in the world.",
    "Pele is the only soccer player to win three FIFA World Cups.",
    "The first cricket test match was played between England and Australia in 1877.",
    "Golf originated in Scotland during the 15th century.",
    "Serena Williams has won 23 Grand Slam singles titles.",
    "The Stanley Cup is the oldest trophy in North American professional sports.",
    "Lionel Messi and Cristiano Ronaldo are considered two of the greatest soccer players of all time.",
    "Muhammad Ali was the first boxer to win the heavyweight title three times.",
    "The first Olympic Games to feature women’s events was in 1900.",
    "The Indianapolis 500 is one of the most famous car races in the world.",
    "Rugby was first introduced at the 1823 Rugby School in England.",
    "The Ashes is a historic cricket series played between England and Australia.",
    "LeBron James is the youngest player to reach 30,000 career points in the NBA.",
    "The 1930 FIFA World Cup was the first-ever World Cup and was hosted by Uruguay.",
    "The New York Yankees have won more World Series titles than any other team in Major League Baseball.",
    "The sport of badminton was derived from a game called 'poona' played in India.",
    "The Triple Crown in horse racing includes the Kentucky Derby, Preakness Stakes, and Belmont Stakes.",
    "The first Winter Olympics were held in Chamonix, France, in 1924.",
    "Roger Federer has spent more weeks as world number one than any other tennis player.",
    "The first recorded soccer match took place in England in 1863.",
    "Formula One driver Lewis Hamilton has won seven World Championships.",
    "The term 'hat trick' originated in cricket and refers to taking three wickets in consecutive balls.",
    "The Harlem Globetrotters are a famous exhibition basketball team known for entertaining fans.",
    "Sachin Tendulkar is the only cricketer to score 100 international centuries.",
    "The NFL team Green Bay Packers is owned by its fans.",
    "Tiger Woods became the youngest golfer to win the Masters Tournament at age 21.",
    "The Ryder Cup is a biennial golf competition between teams from Europe and the United States.",
    "The first recorded tennis game was played in France in the 12th century.",
    "Diego Maradona’s 'Hand of God' goal is one of the most controversial moments in soccer history.",
    "Hockey pucks are frozen before games to reduce bouncing on the ice.",
    "Michael Phelps is the most decorated Olympian of all time with 28 medals.",
    "The first recorded use of the term 'home run' in baseball was in 1856.",
    "The Boston Red Sox famously broke an 86-year championship drought by winning the 2004 World Series.",
    "The fastest goal in soccer history was scored just 2.8 seconds after kickoff.",
    "Cycling has been an Olympic sport since the first modern Games in 1896.",
    "The Rugby World Cup is held every four years, with New Zealand being the most successful team.",
    "The FIFA Women’s World Cup was first held in 1991 and was won by the United States.",
    "The first professional football player in the United States was William 'Pudge' Heffelfinger.",
    "Wimbledon is the only Grand Slam tournament still played on grass courts.",
    "The Stanley Cup has a unique tradition of being passed around to the winning players and staff.",
    "The first recorded boxing match took place in London in 1681.",
    "There are over 7,000 languages spoken worldwide today.",
    "Mandarin Chinese is the most spoken language in the world by native speakers.",
    "English is the most widely spoken language across the globe when combining native and non-native speakers.",
    "The first written language is believed to be Sumerian, dating back to 3100 BCE.",
    "The longest word in English is pneumonoultramicroscopicsilicovolcanoconiosis.",
    "The dot over the letter 'i' and 'j' is called a tittle.",
    "The term 'alphabet' comes from the first two letters of the Greek alphabet, alpha and beta.",
    "French was the official language of England for over 300 years after the Norman Conquest.",
    "The Cherokee writing system was invented by a single man, Sequoyah, in the early 19th century.",
    "Languages evolve, and the English spoken during Shakespeare’s time is called Early Modern English.",
    "The Basque language, spoken in Spain and France, is unrelated to any other known language.",
    "In Japanese, there are three writing systems: kanji, hiragana, and katakana.",
    "Sanskrit is considered one of the oldest known languages still in use today.",
    "The word 'emoji' is derived from Japanese and means 'picture character.'",
    "Arabic is written from right to left, but its numbers are written from left to right.",
    "Sign languages have their own grammar and syntax, and American Sign Language is unrelated to English.",
    "Icelandic has remained largely unchanged for over 1,000 years.",
    "Swahili, a Bantu language, is widely spoken across East Africa and includes many loanwords from Arabic.",
    "The longest palindrome in English is 'tattarrattat,' coined by James Joyce in his novel Ulysses.",
    "German is known for its compound words, including the famous word 'schadenfreude.'",
    "Pirahã, spoken in the Amazon, has one of the smallest known phoneme inventories of any language.",
    "Finnish has no future tense; context determines whether actions are in the past, present, or future.",
    "The Navajo language was used as a secret code by the U.S. military during World War II.",
    "Esperanto is an artificial language created in 1887 to foster international communication.",
    "The word 'OK' is one of the most universally recognized words across languages.",
    "Hebrew was revived as a spoken language in the 19th century after centuries of being used only in writing.",
    "Greek has been continuously spoken for over 3,000 years.",
    "The Welsh town of Llanfair­pwllgwyngyll­gogery­chwyrn­drobwll­llan­tysilio­gogo­goch has one of the longest place names in the world.",
    "Languages like Chinese are tonal, meaning the pitch or intonation of a word can change its meaning.",
    "Italian is considered the closest living language to Latin.",
    "Inuit languages have multiple words for snow, reflecting the Arctic environment.",
    "The word 'alphabet' exists in every major language derived from Greek or Latin scripts.",
    "Turkish is an agglutinative language, meaning words are formed by adding multiple suffixes to root words.",
    "The Rosetta Stone helped decode Egyptian hieroglyphs by comparing them to Greek.",
    "Zulu, a language spoken in South Africa, includes distinctive clicking sounds in its pronunciation.",
    "The most translated document in the world is the Universal Declaration of Human Rights.",
    "French is the official language of 29 countries across multiple continents.",
    "Malay is spoken in several countries and is known as Bahasa Malaysia, Bahasa Indonesia, or simply Bahasa.",
    "The only country with no official language is the United States.",
    "The word 'quiz' was allegedly invented as part of a bet to create a nonsense word that would catch on.",
    "Russian is written in the Cyrillic script, which is used by several Slavic languages.",
    "The first dictionary of the English language was compiled by Samuel Johnson in 1755.",
    "Hawaiian has only 13 letters in its alphabet.",
    "Many African languages, like Xhosa, include click consonants in their phonology.",
    "The Irish language uses the Roman alphabet but has unique diacritical marks like the fada.",
    "Hindi and Urdu are mutually intelligible spoken languages but use entirely different scripts.",
    "The Klingon language was invented for the Star Trek series and is now spoken by enthusiasts worldwide.",
    "The Thai alphabet is one of the longest in the world, with 44 consonants and 32 vowels.",
    "Linguists estimate that a language dies out approximately every two weeks.",
    "The Japanese word 'tsundoku' refers to the act of buying books and not reading them.",
    "Some languages, like Pirahã, have no fixed words for numbers or quantities.",
    "Walking just 30 minutes a day can significantly improve your cardiovascular health.",
    "The human brain is about 73% water, and even mild dehydration can affect its performance.",
    "Muscle tissue burns more calories than fat, even at rest.",
    "Regular exercise can boost your immune system by improving circulation and reducing inflammation.",
    "The average adult should get at least 7-8 hours of sleep each night for optimal health.",
    "The heart pumps about 2,000 gallons of blood through your body every day.",
    "Vitamin D is often called the 'sunshine vitamin' because your body produces it in response to sunlight.",
    "Yoga can help reduce stress, improve flexibility, and increase overall strength.",
    "The largest muscle in the body is the gluteus maximus, located in the buttocks.",
    "Laughter has been shown to reduce stress hormones and improve immune function.",
    "Sitting for long periods is considered as harmful to your health as smoking.",
    "Drinking enough water daily can help improve energy levels and concentration.",
    "The human body contains about 206 bones, and over half of them are in the hands and feet.",
    "Chewing gum can help reduce stress and improve focus in some people.",
    "Your body produces more sweat to cool down when you are physically fit.",
    "The average person takes about 7,500 steps a day, which is roughly 5 kilometers.",
    "Eating too much sugar can weaken your immune system for hours after consumption.",
    "The skin is the largest organ in the human body.",
    "High-intensity interval training (HIIT) can burn more calories in a shorter time than traditional workouts.",
    "Green tea is packed with antioxidants that can help boost metabolism and improve heart health.",
    "The average adult breathes about 20,000 times per day.",
    "Endorphins released during exercise can act as natural painkillers and mood elevators.",
    "A lack of sleep can increase your risk of obesity, diabetes, and heart disease.",
    "Stretching before and after exercise can reduce muscle soreness and improve flexibility.",
    "The human body replaces most of its cells every seven to ten years.",
    "Swimming is a full-body workout that improves cardiovascular health and builds muscle strength.",
    "Eating breakfast can help jumpstart your metabolism and improve concentration.",
    "Regular meditation has been shown to reduce anxiety and improve emotional well-being.",
    "The average heart beats about 100,000 times a day.",
    "A strong core can help improve posture and reduce back pain.",
    "Exercise can help increase the size of the hippocampus, a brain region important for memory.",
    "Processed foods often contain added sugars, unhealthy fats, and high levels of sodium.",
    "Drinking water before meals can help reduce calorie intake and promote weight loss.",
    "Cycling is a low-impact exercise that improves cardiovascular health and strengthens leg muscles.",
    "Protein is essential for muscle repair and growth after exercise.",
    "The average person burns about 50 calories per hour while sleeping.",
    "Eating fiber-rich foods can help regulate digestion and reduce cholesterol levels.",
    "Chronic stress can lead to weight gain, particularly in the abdominal area.",
    "Regular strength training can help prevent muscle loss as you age.",
    "Your metabolism naturally slows down as you get older, especially after age 30.",
    "The human body is capable of producing its own vitamin C in some animals, but not in humans.",
    "Overtraining can lead to fatigue, injuries, and reduced performance.",
    "The World Health Organization recommends at least 150 minutes of moderate exercise per week.",
    "Your bones are constantly being broken down and rebuilt throughout your life.",
    "Dark chocolate contains antioxidants that can improve heart health when consumed in moderation.",
    "Deep breathing exercises can help lower blood pressure and reduce stress.",
    "Bananas are an excellent source of potassium, which helps regulate blood pressure.",
    "Exercise can help reduce the risk of developing dementia and Alzheimer's disease.",
    "Mental health is just as important as physical health for overall well-being.",
    "Eating a rainbow of fruits and vegetables ensures you get a variety of nutrients.",
    "Even light physical activity, like gardening, can improve mental health and reduce stress.",
    "The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones.",
    "Pi is an irrational number, meaning it goes on forever without repeating.",
    "The human body contains about 37 trillion cells.",
    "Water expands when it freezes, making ice less dense than liquid water.",
    "The speed of light in a vacuum is approximately 299,792 kilometers per second.",
    "Zero was first used as a number in ancient India around the 5th century.",
    "The Milky Way galaxy is home to over 100 billion stars.",
    "Atoms are 99.99%\ empty space.",
    "The human brain has about 86 billion neurons.",
    "A light year is the distance light travels in one year, approximately 9.46 trillion kilometers.",
    "The largest prime number discovered so far has over 24 million digits.",
    "There are more possible iterations of a chess game than atoms in the observable universe.",
    "E = mc², Einstein’s famous equation, describes the relationship between energy and mass.",
    "DNA stands for deoxyribonucleic acid, the molecule that carries genetic information.",
    "The Earth’s core is as hot as the surface of the sun.",
    "The Great Pyramid of Giza was originally covered in smooth, white limestone.",
    "The area of a circle is calculated as π multiplied by the radius squared.",
    "The human heart beats about 2.5 billion times in an average lifetime.",
    "The periodic table has 118 confirmed elements.",
    "Venus is the hottest planet in the solar system, even though Mercury is closer to the sun.",
    "The number one is neither a prime number nor a composite number.",
    "The element helium was first discovered in the sun before it was found on Earth.",
    "A googol is the digit 1 followed by 100 zeros.",
    "A bolt of lightning is five times hotter than the surface of the sun.",
    "Mount Everest grows by about 4 millimeters each year due to tectonic activity.",
    "The first computer was invented in 1943 and was called the ENIAC.",
    "Jupiter is so massive that it has over 70 known moons.",
    "Sound travels faster through water than through air.",
    "The human genome contains about 3 billion base pairs.",
    "The Andromeda galaxy is on a collision course with the Milky Way.",
    "The number 1729 is called a 'taxicab number' because it is the smallest number expressible as the sum of two cubes in two different ways.",
    "The double-helix structure of DNA was discovered by Watson and Crick in 1953.",
    "Sharks existed before trees and dinosaurs.",
    "Oxygen makes up about 21%\ of Earth's atmosphere.",
    "Black holes are regions of space where gravity is so strong that nothing, not even light, can escape.",
    "The Richter scale measures the magnitude of earthquakes.",
    "The golden ratio, approximately 1.618, appears frequently in nature and art.",
    "A nanometer is one-billionth of a meter.",
    "The Earth rotates at a speed of about 1,600 kilometers per hour at the equator.",
    "The moon takes about 27.3 days to orbit the Earth.",
    "It is never too late to be what you might have been. George Eliot",
    "What you do today can improve all your tomorrows. Ralph Marston",
    "Don’t let the fear of losing be greater than the excitement of winning. Robert Kiyosaki",
    "An unexamined life is not worth living. Socrates",
    "Do not fear failure but rather fear not trying. Roy T. Bennett",
    "Limit your 'always' and your 'nevers.' Amy Poehler",
    "Success is liking yourself, liking what you do, and liking how you do it. Maya Angelou",
    "Turn your wounds into wisdom. Oprah Winfrey",
    "Happiness is not by chance, but by choice. Jim Rohn",
    "Success is the sum of small efforts, repeated day in and day out. Robert Collier",
    "If you want to lift yourself up, lift up someone else. Booker T. Washington",
    "The only way to achieve the impossible is to believe it is possible. Charles Kingsleigh",
    "We know what we are, but know not what we may be. William Shakespeare",
    "Nothing is impossible, the word itself says, 'I’m possible!' Audrey Hepburn",
    "The mind is everything. What you think you become. Buddha",
    "The greatest wealth is to live content with little. Plato",
    "Do not follow where the path may lead. Go instead where there is no path and leave a trail. Ralph Waldo Emerson",
    "Dream as if you’ll live forever. Live as if you’ll die today. James Dean",
    "The best revenge is massive success. Frank Sinatra",
    "We are what we repeatedly do. Excellence, then, is not an act, but a habit. Aristotle",
    "You can’t use up creativity. The more you use, the more you have. Maya Angelou",
    "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful. Albert Schweitzer",
    "Challenges are what make life interesting, and overcoming them is what makes life meaningful. Joshua J. Marine",
    "The only impossible journey is the one you never begin. Tony Robbins",
    "Happiness depends upon ourselves. Aristotle",
    "Your time is limited, so don’t waste it living someone else’s life. Steve Jobs",
    "Be the change that you wish to see in the world. Mahatma Gandhi",
    "Fall seven times and stand up eight. Japanese Proverb",
    "Whatever you are, be a good one. Abraham Lincoln",
    "I can’t change the direction of the wind, but I can adjust my sails to always reach my destination. Jimmy Dean",
    "The Olympic Games originated in ancient Greece over 2,700 years ago.",
    "The FIFA World Cup is the most-watched sports event in the world.",
    "Basketball was invented in 1891 by Dr. James Naismith.",
    "Cricket is the second most popular sport in the world after soccer.",
    "The Wimbledon Championships is the oldest tennis tournament in the world.",
    "The Boston Marathon is the oldest annual marathon, first held in 1897.",
    "Baseball is known as America’s national pastime.",
    "Usain Bolt holds the world record for the 100-meter sprint.",
    "The first Super Bowl was played in 1967.",
    "Michael Jordan won six NBA championships with the Chicago Bulls.",
    "The Tour de France is the most prestigious cycling race in the world.",
    "Pele is the only soccer player to win three FIFA World Cups.",
    "The first cricket test match was played between England and Australia in 1877.",
    "Golf originated in Scotland during the 15th century.",
    "Serena Williams has won 23 Grand Slam singles titles.",
    "The Stanley Cup is the oldest trophy in North American professional sports.",
    "Lionel Messi and Cristiano Ronaldo are considered two of the greatest soccer players of all time.",
    "Muhammad Ali was the first boxer to win the heavyweight title three times.",
    "The first Olympic Games to feature women’s events was in 1900.",
    "The Indianapolis 500 is one of the most famous car races in the world.",
    "Rugby was first introduced at the 1823 Rugby School in England.",
    "The Ashes is a historic cricket series played between England and Australia.",
    "LeBron James is the youngest player to reach 30,000 career points in the NBA.",
    "The 1930 FIFA World Cup was the first-ever World Cup and was hosted by Uruguay.",
    "The New York Yankees have won more World Series titles than any other team in Major League Baseball.",
    "The sport of badminton was derived from a game called 'poona' played in India.",
    "The Triple Crown in horse racing includes the Kentucky Derby, Preakness Stakes, and Belmont Stakes.",
    "The first Winter Olympics were held in Chamonix, France, in 1924.",
    "Roger Federer has spent more weeks as world number one than any other tennis player.",
    "The first recorded soccer match took place in England in 1863.",
    "Formula One driver Lewis Hamilton has won seven World Championships.",
    "The term 'hat trick' originated in cricket and refers to taking three wickets in consecutive balls.",
    "The Harlem Globetrotters are a famous exhibition basketball team known for entertaining fans.",
    "Sachin Tendulkar is the only cricketer to score 100 international centuries.",
    "The NFL team Green Bay Packers is owned by its fans.",
    "Tiger Woods became the youngest golfer to win the Masters Tournament at age 21.",
    "The Ryder Cup is a biennial golf competition between teams from Europe and the United States.",
    "The first recorded tennis game was played in France in the 12th century.",
    "Diego Maradona’s 'Hand of God' goal is one of the most controversial moments in soccer history.",
    "Hockey pucks are frozen before games to reduce bouncing on the ice.",
    "Michael Phelps is the most decorated Olympian of all time with 28 medals.",
    "The first recorded use of the term 'home run' in baseball was in 1856.",
    "The Boston Red Sox famously broke an 86-year championship drought by winning the 2004 World Series.",
    "The fastest goal in soccer history was scored just 2.8 seconds after kickoff.",
    "Cycling has been an Olympic sport since the first modern Games in 1896.",
    "The Rugby World Cup is held every four years, with New Zealand being the most successful team.",
    "The FIFA Women’s World Cup was first held in 1991 and was won by the United States.",
    "The first professional football player in the United States was William 'Pudge' Heffelfinger.",
    "Wimbledon is the only Grand Slam tournament still played on grass courts.",
    "The Stanley Cup has a unique tradition of being passed around to the winning players and staff.",
    "The first recorded boxing match took place in London in 1681.",
    "There are over 7,000 languages spoken worldwide today.",
    "Mandarin Chinese is the most spoken language in the world by native speakers.",
    "English is the most widely spoken language across the globe when combining native and non-native speakers.",
    "The first written language is believed to be Sumerian, dating back to 3100 BCE.",
    "The longest word in English is pneumonoultramicroscopicsilicovolcanoconiosis.",
    "The dot over the letter 'i' and 'j' is called a tittle.",
    "The term 'alphabet' comes from the first two letters of the Greek alphabet, alpha and beta.",
    "French was the official language of England for over 300 years after the Norman Conquest.",
    "The Cherokee writing system was invented by a single man, Sequoyah, in the early 19th century.",
    "Languages evolve, and the English spoken during Shakespeare’s time is called Early Modern English.",
    "The Basque language, spoken in Spain and France, is unrelated to any other known language.",
    "In Japanese, there are three writing systems: kanji, hiragana, and katakana.",
    "Sanskrit is considered one of the oldest known languages still in use today.",
    "The word 'emoji' is derived from Japanese and means 'picture character.'",
    "Arabic is written from right to left, but its numbers are written from left to right.",
    "Sign languages have their own grammar and syntax, and American Sign Language is unrelated to English.",
    "Icelandic has remained largely unchanged for over 1,000 years.",
    "Swahili, a Bantu language, is widely spoken across East Africa and includes many loanwords from Arabic.",
    "The longest palindrome in English is 'tattarrattat,' coined by James Joyce in his novel Ulysses.",
    "German is known for its compound words, including the famous word 'schadenfreude.'",
    "Pirahã, spoken in the Amazon, has one of the smallest known phoneme inventories of any language.",
    "Finnish has no future tense; context determines whether actions are in the past, present, or future.",
    "The Navajo language was used as a secret code by the U.S. military during World War II.",
    "Esperanto is an artificial language created in 1887 to foster international communication.",
    "The word 'OK' is one of the most universally recognized words across languages.",
    "Hebrew was revived as a spoken language in the 19th century after centuries of being used only in writing.",
    "Greek has been continuously spoken for over 3,000 years.",
    "The Welsh town of Llanfair­pwllgwyngyll­gogery­chwyrn­drobwll­llan­tysilio­gogo­goch has one of the longest place names in the world.",
    "Languages like Chinese are tonal, meaning the pitch or intonation of a word can change its meaning.",
    "Italian is considered the closest living language to Latin.",
    "Inuit languages have multiple words for snow, reflecting the Arctic environment.",
    "The word 'alphabet' exists in every major language derived from Greek or Latin scripts.",
    "Turkish is an agglutinative language, meaning words are formed by adding multiple suffixes to root words.",
    "The Rosetta Stone helped decode Egyptian hieroglyphs by comparing them to Greek.",
    "Zulu, a language spoken in South Africa, includes distinctive clicking sounds in its pronunciation.",
    "The most translated document in the world is the Universal Declaration of Human Rights.",
    "French is the official language of 29 countries across multiple continents.",
    "Malay is spoken in several countries and is known as Bahasa Malaysia, Bahasa Indonesia, or simply Bahasa.",
    "The only country with no official language is the United States.",
    "The word 'quiz' was allegedly invented as part of a bet to create a nonsense word that would catch on.",
    "Russian is written in the Cyrillic script, which is used by several Slavic languages.",
    "The first dictionary of the English language was compiled by Samuel Johnson in 1755.",
    "Hawaiian has only 13 letters in its alphabet.",
    "Many African languages, like Xhosa, include click consonants in their phonology.",
    "The Irish language uses the Roman alphabet but has unique diacritical marks like the fada.",
    "Hindi and Urdu are mutually intelligible spoken languages but use entirely different scripts.",
    "The Klingon language was invented for the Star Trek series and is now spoken by enthusiasts worldwide.",
    "The Thai alphabet is one of the longest in the world, with 44 consonants and 32 vowels.",
    "Linguists estimate that a language dies out approximately every two weeks.",
    "The Japanese word 'tsundoku' refers to the act of buying books and not reading them.",
    "Some languages, like Pirahã, have no fixed words for numbers or quantities.",
    "Walking just 30 minutes a day can significantly improve your cardiovascular health.",
    "The human brain is about 73% water, and even mild dehydration can affect its performance.",
    "Muscle tissue burns more calories than fat, even at rest.",
    "Regular exercise can boost your immune system by improving circulation and reducing inflammation.",
    "The average adult should get at least 7-8 hours of sleep each night for optimal health.",
    "The heart pumps about 2,000 gallons of blood through your body every day.",
    "Vitamin D is often called the 'sunshine vitamin' because your body produces it in response to sunlight.",
    "Yoga can help reduce stress, improve flexibility, and increase overall strength.",
    "The largest muscle in the body is the gluteus maximus, located in the buttocks.",
    "Laughter has been shown to reduce stress hormones and improve immune function.",
    "Sitting for long periods is considered as harmful to your health as smoking.",
    "Drinking enough water daily can help improve energy levels and concentration.",
    "The human body contains about 206 bones, and over half of them are in the hands and feet.",
    "Chewing gum can help reduce stress and improve focus in some people.",
    "Your body produces more sweat to cool down when you are physically fit.",
    "The average person takes about 7,500 steps a day, which is roughly 5 kilometers.",
    "Eating too much sugar can weaken your immune system for hours after consumption.",
    "The skin is the largest organ in the human body.",
    "High-intensity interval training (HIIT) can burn more calories in a shorter time than traditional workouts.",
    "Green tea is packed with antioxidants that can help boost metabolism and improve heart health.",
    "The average adult breathes about 20,000 times per day.",
    "Endorphins released during exercise can act as natural painkillers and mood elevators.",
    "A lack of sleep can increase your risk of obesity, diabetes, and heart disease.",
    "Stretching before and after exercise can reduce muscle soreness and improve flexibility.",
    "The human body replaces most of its cells every seven to ten years.",
    "Swimming is a full-body workout that improves cardiovascular health and builds muscle strength.",
    "Eating breakfast can help jumpstart your metabolism and improve concentration.",
    "Regular meditation has been shown to reduce anxiety and improve emotional well-being.",
    "The average heart beats about 100,000 times a day.",
    "A strong core can help improve posture and reduce back pain.",
    "Exercise can help increase the size of the hippocampus, a brain region important for memory.",
    "Processed foods often contain added sugars, unhealthy fats, and high levels of sodium.",
    "Drinking water before meals can help reduce calorie intake and promote weight loss.",
    "Cycling is a low-impact exercise that improves cardiovascular health and strengthens leg muscles.",
    "Protein is essential for muscle repair and growth after exercise.",
    "The average person burns about 50 calories per hour while sleeping.",
    "Eating fiber-rich foods can help regulate digestion and reduce cholesterol levels.",
    "Chronic stress can lead to weight gain, particularly in the abdominal area.",
    "Regular strength training can help prevent muscle loss as you age.",
    "Your metabolism naturally slows down as you get older, especially after age 30.",
    "The human body is capable of producing its own vitamin C in some animals, but not in humans.",
    "Overtraining can lead to fatigue, injuries, and reduced performance.",
    "The World Health Organization recommends at least 150 minutes of moderate exercise per week.",
    "Your bones are constantly being broken down and rebuilt throughout your life.",
    "Dark chocolate contains antioxidants that can improve heart health when consumed in moderation.",
    "Deep breathing exercises can help lower blood pressure and reduce stress.",
    "Bananas are an excellent source of potassium, which helps regulate blood pressure.",
    "Exercise can help reduce the risk of developing dementia and Alzheimer's disease.",
    "Mental health is just as important as physical health for overall well-being.",
    "Eating a rainbow of fruits and vegetables ensures you get a variety of nutrients.",
    "Even light physical activity, like gardening, can improve mental health and reduce stress.",
    "The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones.",
    "Pi is an irrational number, meaning it goes on forever without repeating.",
    "The human body contains about 37 trillion cells.",
    "Water expands when it freezes, making ice less dense than liquid water.",
    "The speed of light in a vacuum is approximately 299,792 kilometers per second.",
    "Zero was first used as a number in ancient India around the 5th century.",
    "The Milky Way galaxy is home to over 100 billion stars.",
    "Atoms are 99.99%\ empty space.",
    "The human brain has about 86 billion neurons.",
    "A light year is the distance light travels in one year, approximately 9.46 trillion kilometers.",
    "The largest prime number discovered so far has over 24 million digits.",
    "There are more possible iterations of a chess game than atoms in the observable universe.",
    "E = mc², Einstein’s famous equation, describes the relationship between energy and mass.",
    "DNA stands for deoxyribonucleic acid, the molecule that carries genetic information.",
    "The Earth’s core is as hot as the surface of the sun.",
    "The Great Pyramid of Giza was originally covered in smooth, white limestone.",
    "The area of a circle is calculated as π multiplied by the radius squared.",
    "The human heart beats about 2.5 billion times in an average lifetime.",
    "The periodic table has 118 confirmed elements.",
    "Venus is the hottest planet in the solar system, even though Mercury is closer to the sun.",
    "The number one is neither a prime number nor a composite number.",
    "The element helium was first discovered in the sun before it was found on Earth.",
    "A googol is the digit 1 followed by 100 zeros.",
    "A bolt of lightning is five times hotter than the surface of the sun.",
    "Mount Everest grows by about 4 millimeters each year due to tectonic activity.",
    "The first computer was invented in 1943 and was called the ENIAC.",
    "Jupiter is so massive that it has over 70 known moons.",
    "Sound travels faster through water than through air.",
    "The human genome contains about 3 billion base pairs.",
    "The Andromeda galaxy is on a collision course with the Milky Way.",
    "The number 1729 is called a 'taxicab number' because it is the smallest number expressible as the sum of two cubes in two different ways.",
    "The double-helix structure of DNA was discovered by Watson and Crick in 1953.",
    "Sharks existed before trees and dinosaurs.",
    "Oxygen makes up about 21%\ of Earth's atmosphere.",
    "Black holes are regions of space where gravity is so strong that nothing, not even light, can escape.",
    "The Richter scale measures the magnitude of earthquakes.",
    "The golden ratio, approximately 1.618, appears frequently in nature and art.",
    "A nanometer is one-billionth of a meter.",
    "The Earth rotates at a speed of about 1,600 kilometers per hour at the equator.",
    "The moon takes about 27.3 days to orbit the Earth.",]


def clear_screen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def calculate_wpm(start_time, end_time, total_words):
    """Calculate words per minute (WPM)."""
    if total_words == 0:
        return 0
    elapsed_time = end_time - start_time  # Time in seconds
    wpm = (total_words / elapsed_time) * 60  # Convert to words per minute
    return round(wpm, 2)

def calculate_accuracy(original_sentences, typed_sentences):
    """Calculate typing accuracy as a percentage."""
    total_correct = 0
    total_words = 0

    for original, typed in zip(original_sentences, typed_sentences):
        original_words = original.split()
        typed_words = typed.split()
        total_words += len(original_words)
        total_correct += sum(1 for o, t in zip(original_words, typed_words) if o == t)

    accuracy = (total_correct / total_words) * 100
    return round(accuracy, 2)

def colorize_typed(original, typed):
    """Colorize the typed words based on correctness."""
    original_words = original.split()
    typed_words = typed.split()
    colored_output = []

    for o, t in zip(original_words, typed_words):
        if o == t:
            colored_output.append(f"\033[1;32m{t}\033[0m")  # Green for correct
        else:
            colored_output.append(f"\033[1;31m{t}\033[0m")  # Red for incorrect

    # Add remaining words from the typed sentence (if any)
    if len(typed_words) > len(original_words):
        for t in typed_words[len(original_words):]:
            colored_output.append(f"\033[1;31m{t}\033[0m")  # Extra words in red

    return " ".join(colored_output)

def display_session_bar_chart(results):
    """Display a bar chart showing all test results in the session."""
    print("\nSession Progress Bar Chart")
    bar_width = 8  # Adjust bar width to align bars over labels
    chart_width = len(results) * bar_width + 10  # Total width of the chart
    print("-" * chart_width)  # Top border spanning the chart

    max_wpm = max(results + [65])  # Ensure at least 65 for proper scaling
    max_height = int((max_wpm // 5 + 1) * 5)  # Round up to nearest multiple of 5

    for row in range(max_height, 0, -5):
        # Add row labels and spacing
        line = f"{str(row).rjust(4)} |"

        # Add bars for each result
        for wpm in results:
            if wpm >= row:
                if wpm < 45:
                    color = "\033[1;31m"  # Red for below average
                elif 45 <= wpm < 65:
                    color = "\033[1;33m"  # Yellow for average
                else:
                    color = "\033[1;32m"  # Green for fast
                line += f"   {color}#\033[0m   "
            else:
                line += "       "  # Empty space for unused bar positions

        # Add thresholds for Fast and Average as continuous lines
        if row == 45:
            print("\033[1;34m" + "-" * chart_width + "\033[0m (Average)")  # Blue line
        elif row == 65:
            print("\033[1;36m" + "-" * chart_width + "\033[0m (Fast)")  # Cyan line

        print(line)

    # Bottom horizontal line
    print("-" * chart_width)

    # Add WPM and Test labels aligned on the same line
    wpm_label = "  WPM".ljust(1)  # Align WPM label with vertical numbers
    test_labels = "".join([f"T{i+1}".center(bar_width) for i in range(len(results))])
    print(wpm_label + " " + test_labels)  # Shift test labels one space left

def typing_test(num_tests=2, sentences_per_test=1, blind_mode=False):
    """Main typing test function."""

    clear_screen()
    print("Typing Speed Test")
    print("-----------------")
    print(f"Number of tests: {num_tests}")
    print(f"Sentences per test: {sentences_per_test}")
    print(f"Blind mode: {'Enabled' if blind_mode else 'Disabled'}")

    session_results = []
    session_accuracies = []
    tests_completed = 0  # Track the number of tests with valid input

    for test_number in range(1, num_tests + 1):
        clear_screen()
        print(f"Typing Speed Test - Test {test_number}/{num_tests}")
        print("-------------------------------")

        # Select random sentences
        selected_sentences = random.sample(sentences, sentences_per_test)
        start_time = time.time()  # Start the timer
        typed_sentences = []
        total_words = 0

        # Display sentences one by one
        valid_input = False  # Track if the user typed valid input
        for i, sentence in enumerate(selected_sentences, start=1):
            clear_screen()
            print(f"Sentence {i}/{sentences_per_test}:")
            print(f"\033[1;33m{sentence}\033[0m")  # Highlight the sentence in yellow

            # Blind mode hides user input
            if blind_mode:
                print("\nType the sentence (input will be hidden):")
                user_input = getpass.getpass("")  # Hidden input
            else:
                user_input = input("\nType the sentence: ").strip()

            # Check if user actually typed something
            if user_input:
                valid_input = True
                typed_sentences.append(user_input)
                total_words += len(sentence.split())
            else:
                typed_sentences.append("")  # To maintain alignment for skipped sentences

        end_time = time.time()  # End the timer

        # Skip results if no valid input was provided
        if not valid_input:
            print("\nNo valid input detected for this test. Test skipped.")
            time.sleep(2)
            continue

        # Calculate results
        wpm = calculate_wpm(start_time, end_time, total_words)
        accuracy = calculate_accuracy(selected_sentences, typed_sentences)
        elapsed_time = round(end_time - start_time, 2)

        # Store the WPM and accuracy for valid tests only
        session_results.append(wpm)
        session_accuracies.append(accuracy)
        tests_completed += 1

        # Display individual test results
        clear_screen()
        print("\nResults")
        print("-------")
        print(f"Test {test_number} - Time: {elapsed_time}s, WPM: {wpm}, Accuracy: {accuracy}%")
        print("\nSentence-by-Sentence Details:")
        for original, typed in zip(selected_sentences, typed_sentences):
            colored_typed = colorize_typed(original, typed)
            max_length = max(len(original), len(typed))
            print(f"{original.ljust(max_length)}")  # Display original sentence
            print(f"{colored_typed.ljust(max_length)}")  # Display typed sentence
            print()

        # Wait briefly before the next test, unless it's the last test
        if test_number <= num_tests:
            time.sleep(2)

    # Handle case where no tests are completed
    if tests_completed == 0:
        clear_screen()
        print("\nSession Results")
        print("----------------")
        print("No tests were completed. Final result is FAIL.")
        return  # Exit without displaying the bar chart

    # Calculate final results
    average_accuracy = sum(session_accuracies) / len(session_accuracies) if session_accuracies else 0
    average_wpm = sum(session_results) / len(session_results) if session_results else 0
    final_result = "PASS" if average_accuracy >= 70 else "FAIL"

    # Display Final Results with Proper Alignment
    clear_screen()
    print("\nFinal Results")
    print("-------------")
    print(f"{'Average Accuracy:'.ljust(25)} {average_accuracy:.2f}%")
    print(f"{'Average Typing Speed:'.ljust(25)} {average_wpm:.2f} WPM")
    print(f"{'Result:'.ljust(25)} \033[1;32m{final_result}\033[0m" if final_result == "PASS" else f"{'Result:'.ljust(25)} \033[1;31m{final_result}\033[0m")
    print()

    # Display bar chart only if at least one test was completed
    display_session_bar_chart(session_results)

# def main():
#     parser = argparse.ArgumentParser(
#         description="Process test parameters with optional blind mode."
#     )
#     parser.add_argument(
#         "tests",
#         type=int,
#         nargs="?",
#         default=2,
#         help="The number of tests to run (default: 2).",
#     )
#     parser.add_argument(
#         "sentences_per_test",
#         type=int,
#         nargs="?",
#         default=1,
#         help="The number of sentences per test (default: 1).",
#     )
#     parser.add_argument(
#         "blind_mode",
#         type=str,
#         nargs="?",
#         default="no",
#         help="Set blind mode to 'y' or 'yes' to enable it (default: no).",
#     )

#     # Parse arguments, silently fallback to defaults for invalid input
#     try:
#         args = parser.parse_args()
#         # Validate inputs and fallback silently if necessary
#         tests = args.tests if isinstance(args.tests, int) else 2
#         sentences_per_test = args.sentences_per_test if isinstance(args.sentences_per_test, int) else 1
#         blind_mode = args.blind_mode if isinstance(args.blind_mode, str) else "no"
#         blind_mode_bool = blind_mode.lower()[0] == "y"
#         typing_test(tests, sentences_per_test, blind_mode_bool)
#     except KeyboardInterrupt:
#         print("\n\nExiting Typing Speed Test...")
#         exit(0)
#     except Exception:
#         # Fallback to default values
#         typing_test()

# if __name__ == "__main__":
#     main()