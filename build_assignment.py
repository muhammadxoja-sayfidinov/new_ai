import zipfile, os

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def esc(t):
    return (t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

def run(text, bold=False, italic=False, sz=22):
    rpr = '<w:rPr>'
    if bold: rpr += '<w:b/>'
    if italic: rpr += '<w:i/>'
    rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
    return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

def para(text='', bold=False, italic=False, sz=22, align=None, after=120, indent=False):
    ppr = '<w:pPr>'
    if align: ppr += f'<w:jc w:val="{align}"/>'
    if indent: ppr += '<w:ind w:firstLine="360"/>'
    ppr += f'<w:spacing w:after="{after}" w:line="276" w:lineRule="auto"/></w:pPr>'
    body = run(text, bold, italic, sz) if text else ''
    return f'<w:p>{ppr}{body}</w:p>'

def heading(text, level=1):
    sizes = {1: 32, 2: 26, 3: 24}
    pb = 240 if level == 1 else 200
    ppr = (f'<w:pPr><w:keepNext/><w:spacing w:before="{pb}" w:after="120"/>'
           f'<w:outlineLvl w:val="{level-1}"/></w:pPr>')
    return f'<w:p>{ppr}{run(text, bold=True, sz=sizes[level])}</w:p>'

def bullet(text):
    ppr = ('<w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
           '<w:spacing w:after="80" w:line="276" w:lineRule="auto"/></w:pPr>')
    return f'<w:p>{ppr}{run(text)}</w:p>'

def pagebreak():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'



def cell(text, width, bold=False, sz=20, shade=None, align=None):
    tcpr = f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>'
    if shade:
        tcpr += f'<w:shd w:val="clear" w:color="auto" w:fill="{shade}"/>'
    tcpr += '<w:vAlign w:val="center"/></w:tcPr>'
    ppr = '<w:pPr>'
    if align: ppr += f'<w:jc w:val="{align}"/>'
    ppr += '<w:spacing w:after="40" w:line="240" w:lineRule="auto"/></w:pPr>'
    body = run(text, bold=bold, sz=sz) if text != '' else ''
    return f'<w:tc>{tcpr}<w:p>{ppr}{body}</w:p></w:tc>'

def table(rows, widths, header_shade='D9E2F3'):
    total = sum(widths)
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    tblpr = (f'<w:tblPr><w:tblW w:w="{total}" w:type="dxa"/>'
             '<w:tblBorders>'
             '<w:top w:val="single" w:sz="4" w:color="808080"/>'
             '<w:left w:val="single" w:sz="4" w:color="808080"/>'
             '<w:bottom w:val="single" w:sz="4" w:color="808080"/>'
             '<w:right w:val="single" w:sz="4" w:color="808080"/>'
             '<w:insideH w:val="single" w:sz="4" w:color="808080"/>'
             '<w:insideV w:val="single" w:sz="4" w:color="808080"/>'
             '</w:tblBorders><w:tblLook w:val="04A0"/></w:tblPr>')
    out = f'<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>'
    for ri, row in enumerate(rows):
        is_head = (ri == 0)
        cells = ''
        for ci, txt in enumerate(row):
            shade = header_shade if is_head else None
            al = 'center' if is_head else (None if ci == 0 else 'center')
            cells += cell(txt, widths[ci], bold=is_head, shade=shade, align=al)
        trpr = '<w:trPr><w:tblHeader/></w:trPr>' if is_head else ''
        out += f'<w:tr>{trpr}{cells}</w:tr>'
    out += '</w:tbl>'
    return out



B = []

# ---------------- COVER PAGE ----------------
B.append(para())
B.append(para())
B.append(para('Level 5 | Unit: 21 | Emerging Technologies', bold=True, sz=28, align='center'))
B.append(para())
B.append(para('Emerging Technologies: Impact, Adoption and Local Context in Uzbekistan',
              bold=True, sz=36, align='center'))
B.append(para())
B.append(para('5G (Fifth Generation Mobile Network)', bold=True, sz=30, align='center'))
B.append(para())
B.append(para())
B.append(para('[Your Full Name]', bold=True, sz=26, align='center'))
B.append(para('Assessor: Konstantin Drygin', sz=24, align='center'))
B.append(para('Group ID: [your group]', sz=24, align='center'))
B.append(para('Student ID: [your ID]', sz=24, align='center'))
B.append(para('Submission Date: 05.06.2026', sz=24, align='center'))
B.append(pagebreak())



# ---------------- DECLARATION ----------------
B.append(heading('BTEC Learner Assessment Submission and Declaration', 1))
B.append(para('When submitting evidence for assessment, each learner must sign a declaration '
              'confirming that the work is their own.', sz=20))
decl = [
    ['Field', 'Detail'],
    ['Learner (Student) ID', '[your ID]'],
    ['Assessor Name', 'Konstantin Drygin'],
    ['BTEC Programme Title', 'Pearson BTEC Higher Nationals in Information Technologies'],
    ['Unit or Component Number and Title', 'Unit 21: Emerging Technologies'],
    ['Assignment Title', 'Emerging Technologies: Impact, Adoption and Local Context in Uzbekistan'],
    ['Date Assignment Submitted', '05.06.2026'],
]
B.append(table(decl, [3200, 6000]))
B.append(para())
B.append(para('I certify that the work submitted for this assignment is my own. I have clearly '
              'referenced any sources used in the work. I understand that false declaration is a '
              'form of malpractice.', sz=20))
B.append(para())
B.append(para('Learner signature: ______________________                 Date: 05.06.2026', sz=20))
B.append(pagebreak())

# ---------------- TABLE OF CONTENTS ----------------
B.append(heading('Table of Contents', 1))
for i, t in enumerate(['Introduction', 'Technology Overview', 'Economic Factors',
                       'Technology Connections', 'Political and Social Factors',
                       'Conclusion \u2013 Future Impact', 'Presentation', 'Reference List'], 1):
    B.append(para(f'{i}.  {t}', sz=22))
B.append(pagebreak())



# ================= 1. INTRODUCTION =================
B.append(heading('Introduction', 1))
B.append(para(
    'An emerging technology is a new and innovative solution that grows quickly and creates a high '
    'impact across many industries, often changing the way businesses and ordinary people do things '
    'every day (Schwab, 2016). The main characteristics are clear: it is new and innovative, it shows '
    'fast growth, and it has a strong potential impact on society. 5G, the fifth generation of mobile '
    'networks, fits this description very well. It is still growing rapidly across the world and is only '
    'now reaching early commercial use in Uzbekistan. 5G delivers much faster speeds than 4G, very low '
    'latency of around 1\u20135 milliseconds, and the ability to connect a huge number of devices at once. '
    'Because of this, it directly supports the goals of the \u201cDigital Uzbekistan \u2013 2030\u201d strategy, '
    'which is why I chose it as my emerging technology.', indent=True))

# ================= 2. TECHNOLOGY OVERVIEW =================
B.append(heading('Technology Overview', 1))
B.append(para(
    'Slow internet during a video call, buffering while streaming, or a factory robot that cannot react '
    'in real time \u2013 these are everyday limits of older mobile networks. 5G technology was designed to '
    'remove these limits by combining very high speed, very low delay, and massive device capacity in '
    'one network. Below I explain how it actually works, where it is used today, and what its real '
    'strengths and weaknesses are.', indent=True))



B.append(heading('How the Technology Works', 2))
B.append(para(
    'A 5G network moves data over three groups of radio frequencies. Low-band spectrum (below 1 GHz) '
    'travels far and goes through walls, so it is used for wide coverage. Mid-band (around 3.4\u20133.8 GHz) '
    'gives a strong balance of speed and range and is the main \u201cworkhorse\u201d band for most operators. '
    'High-band millimetre wave (24 GHz and above) gives extremely high speed but only over short distances '
    '(GSMA Intelligence, 2026).', indent=True))
B.append(para(
    'On top of the spectrum, 5G uses several smart techniques. Massive MIMO uses dozens of small antennas '
    'on one base station to serve many users at the same time. Beamforming then focuses the signal '
    'directly towards each device instead of spreading it in every direction, which saves energy and '
    'improves quality. The most important business feature is network slicing: an operator can split one '
    'physical network into several virtual networks, so a hospital, a factory and ordinary phone users '
    'can each get a slice with the exact speed and reliability they need. In Uzbekistan, the core network '
    'connects to national infrastructure and increasingly to edge computing sites so that data is '
    'processed close to the user for the lowest possible delay.', indent=True))



B.append(heading('Where It Is Used Today', 2))
B.append(para(
    'Globally, 5G is already used in many sectors. In healthcare it supports remote monitoring and even '
    'remote surgery because of its low latency. In manufacturing, private 5G networks connect robots and '
    'sensors for real-time automation. In entertainment, cloud-gaming services such as Xbox Cloud Gaming '
    'and NVIDIA GeForce Now stream high-quality games to phones. Large vendors lead these projects \u2013 for '
    'example Ericsson with Deutsche Telekom in Germany, Samsung with Verizon in the United States, and '
    'Huawei and ZTE across Asia.', indent=True))
B.append(para(
    'Uzbekistan is moving quickly from pilots to commercial service. Ucell commercially launched 5G in '
    'the city of Termez, installing new base stations in the centre, transport hubs and densely built '
    'areas (CB Insights, 2026). The smaller operator Perfectum partnered with Nokia to build a 5G '
    'standalone network supported by a single trusted vendor (Times of Central Asia, 2024). At the '
    'GSMA M360 Eurasia summit held in Samarkand in May 2026, Viasat even demonstrated the first '
    'direct-to-device satellite messaging on an ordinary Android phone in Uzbekistan, showing how '
    'serious the country has become about next-generation connectivity (Times of Central Asia, 2026).',
    indent=True))



B.append(heading('Advantages and Disadvantages', 2))
B.append(para('The main advantages of 5G are:', sz=22))
B.append(bullet('Very high speed \u2013 download speeds of 1\u201310 Gbps allow real-time tasks such as '
                'telemedicine and self-driving cars that 4G simply cannot handle.'))
B.append(bullet('Low latency \u2013 a response time of about 1\u20135 ms, compared with 30\u201350 ms on 4G, which '
                'is essential for remote control and automation.'))
B.append(bullet('Massive connectivity \u2013 up to one million devices per square kilometre, which supports '
                'smart-city and Internet of Things projects.'))
B.append(bullet('Network slicing \u2013 operators can sell customised virtual networks to businesses, creating '
                'new income beyond normal phone plans.'))
B.append(bullet('Better energy efficiency per bit, which helps operators cut electricity costs and meet '
                'sustainability goals.'))
B.append(para('However, there are also clear disadvantages:', sz=22))
B.append(bullet('High cost of building the network, because millimetre-wave 5G needs many small base '
                'stations placed close together.'))
B.append(bullet('Weak rural coverage, since high-band signals travel only short distances and struggle to '
                'pass through buildings.'))
B.append(bullet('Expensive devices \u2013 users must buy new 5G phones, which are still costly for many people '
                'in developing markets.'))
B.append(bullet('Security risks, because more connected devices give hackers a larger attack surface.'))
B.append(bullet('Public health worries about radiation, even though the World Health Organization confirms '
                '5G is safe within international limits (WHO, 2020).'))



B.append(heading('Overview Conclusion and Local Context', 2))
B.append(para(
    'To sum up, 5G is powerful because it mixes speed, low latency and huge capacity, although the cost '
    'and coverage problems still need attention. The Uzbekistan context already shows real progress. '
    'First, Ucell completed a large deployment with ZTE of an AI-powered \u201cgreen network\u201d solution that '
    'increased energy efficiency by 10.6% across its network in May 2026 (ZTE, 2026). Second, Beeline '
    'Uzbekistan, owned by the VEON group, upgraded more than 400 base stations during 2025 and raised '
    'average user internet speed by 67.4% (Kursiv Media, 2025a). Third, independent testing by Ookla '
    'found Ucell had the best mobile network in the first half of 2025 with a median download speed of '
    '56.38 Mbps (Ookla, 2025). These cases prove that 5G is not just a future idea in Uzbekistan \u2013 it '
    'is being built right now, which connects directly to the economic factors discussed next.', indent=True))



# ================= 3. ECONOMIC FACTORS =================
B.append(heading('Economic Factors', 1))
B.append(para(
    'Origin and time to market. 5G was developed by global standards bodies (3GPP) and the first '
    'commercial networks went live around 2019. There was a delay between the first idea and mass '
    'adoption because operators first had to buy expensive spectrum and build new equipment. In '
    'Uzbekistan the real take-off is only happening now, after 2023, as affordable 5G phones and '
    'modernised base stations spread across the bigger cities.', indent=True))
B.append(para(
    'Business model and monetization. 5G mainly earns money through three models. The first is consumer '
    'subscriptions, where operators sell faster mobile plans. The second is the platform / network-as-a-'
    'service model, where operators sell dedicated network slices and private 5G networks to factories, '
    'ports and hospitals. The third is an API and edge-computing model, where cloud companies such as '
    'AWS, Microsoft Azure and Google Cloud charge developers for services that run on top of 5G. '
    'Equipment vendors such as Ericsson, Nokia, Huawei and ZTE add a fourth layer by selling hardware '
    'and long-term maintenance contracts to operators (GSMA Intelligence, 2026).', indent=True))



B.append(para(
    'Market size and customers. Globally the 5G infrastructure market was worth about USD 47.44 billion '
    'in 2025 and is expected to reach USD 68.07 billion in 2026, growing at a CAGR of 34.70% (Fortune '
    'Business Insights, 2026). The private 5G network market alone is forecast to jump from USD 4.5 '
    'billion in 2025 to around USD 312.2 billion by 2035 (GlobeNewswire, 2026). In Uzbekistan the picture '
    'is also strong. The whole telecom market doubled between 2020 and 2024 to reach 20.9 trillion soums, '
    'and it grew 18.6% in 2024 \u2013 faster than Kazakhstan or Russia. A joint Nexign and TelecomDaily study '
    'expects Uzbekistan to be the fastest-growing telecom market in the CIS, expanding about 12.7% per '
    'year, driven mainly by 5G (Kursiv Media, 2025b). The mobile-network-operator segment is valued at '
    'roughly USD 0.96 billion in 2025 and should reach USD 1.29 billion by 2030 (Mordor Intelligence, '
    '2025). The customers are individuals (B2C), businesses and factories (B2B), and government smart-'
    'city and e-government projects (G2C), with the B2B private-network segment expected to bring the '
    'highest value per client.', indent=True))



B.append(para(
    'Costs, profit and scalability. The biggest cost of 5G is capital expenditure (CapEx): spectrum '
    'licences, thousands of base stations and fibre links. Operating expenditure (OpEx) is dominated by '
    'electricity, which is exactly why Ucell and ZTE invested in an AI energy-saving system to cut power '
    'use (ZTE, 2026). To become profitable, an operator must balance its Customer Acquisition Cost (CAC) '
    'against the Average Revenue Per User (ARPU). Because basic data prices in Uzbekistan are low \u2013 around '
    'USD 3 per gigabyte on some plans (DialAnyone, 2026) \u2013 operators must grow ARPU through premium 5G '
    'tiers and B2B contracts rather than simple data sales. The good news is that 5G scales well: once '
    'the core is built, the cost of serving each extra user falls sharply, so return on investment is '
    'long-term (about 3\u20135 years) but solid.', indent=True))
B.append(para(
    'Local market conditions and cases. The Uzbek government is actively lowering the cost of entry. In '
    'November 2025 it launched a tax-free zone for major AI and data-centre projects to attract investors '
    '(Euronews, 2025), and a presidential decree gave all licensed operators direct access to '
    'international bandwidth, which cuts wholesale costs (TS2 Tech, 2026). Real local business cases '
    'include the Ucell\u2013ZTE deployment (foreign investment plus technology transfer), the Perfectum\u2013Nokia '
    'standalone 5G build (Times of Central Asia, 2024), and VEON\u2019s new Beeline Network Operations Center '
    'plus its \u201cBuildX\u201d software accelerator in Tashkent (VEON, 2026). Together these show a realistic, '
    'fast-growing 5G economy in Uzbekistan, which links directly to the political and social factors in '
    'the next section.', indent=True))



# ================= 4. TECHNOLOGY CONNECTIONS =================
B.append(heading('Technology Connections', 1))
B.append(para(
    '5G does not work on its own. It sits inside a large ecosystem of older, current and future '
    'technologies, and understanding these links shows where the technology came from and where it is '
    'going.', indent=True))
B.append(para(
    'What it replaces and inherits from. 5G inherits the basic idea of cellular mobile networks and '
    'still relies on a strong fibre-optic backbone for transport. At the same time it gradually replaces '
    '4G LTE for demanding tasks and can even replace fixed broadband in rural areas where laying fibre is '
    'too expensive.', indent=True))
B.append(para(
    'What it depends on. The 5G core depends on Massive MIMO antennas, edge computing and cloud data '
    'centres to deliver low latency, on network slicing to serve different customers, and on the national '
    'fibre network and allocated spectrum from the regulator. In Uzbekistan it also depends on energy-'
    'efficient equipment, which is why the Ucell\u2013ZTE AI power-saving system matters so much (ZTE, 2026).',
    indent=True))
B.append(para(
    'Future convergence. In the coming years 5G will merge with artificial intelligence (for example the '
    'AI RAN energy system already running on Ucell), digital twins for smart cities, and satellite '
    'direct-to-device links such as the Viasat demonstration in Samarkand (Times of Central Asia, 2026). '
    'It will also be the foundation that later evolves into 6G.', indent=True))
B.append(para(
    'The diagram below shows these 23 connected technology blocks in a vertical layout. It should be '
    'exported as a PNG (white background, dark text and lines, light-coloured blocks) using the export '
    'option of the diagram tool \u2013 for example, in mermaid.live choose Actions \u2192 PNG.', italic=True, sz=20))



def codeblock(lines):
    runs = ''
    for i, ln in enumerate(lines):
        runs += (f'<w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
                 f'<w:sz w:val="16"/></w:rPr><w:t xml:space="preserve">{esc(ln)}</w:t></w:r>')
        if i < len(lines) - 1:
            runs += '<w:r><w:br/></w:r>'
    ppr = ('<w:pPr><w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>'
           '<w:spacing w:after="120" w:line="240" w:lineRule="auto"/>'
           '<w:ind w:left="120"/></w:pPr>')
    return f'<w:p>{ppr}{runs}</w:p>'

mermaid = [
    '%%{init: {"theme":"neutral"}}%%',
    'graph TB',
    '    A[5G Core Network]',
    '    A --> B[Massive MIMO Antennas]',
    '    A --> C[Edge Computing]',
    '    A --> D[Cloud Data Centres]',
    '    A --> E[Network Slicing]',
    '    A --> F[National Fibre / UZTELECOM]',
    '    A --> G[Spectrum & Regulator]',
    '    A -.->|replaces| H[4G LTE]',
    '    A -.->|replaces| I[Fixed Broadband Rural]',
    '    A --> J[Internet of Things]',
    '    J --> K[Smart Agriculture]',
    '    J --> L[Industrial Sensors]',
    '    A --> M[Smart Cities]',
    '    A --> N[Autonomous Vehicles / V2X]',
    '    A --> O[Telemedicine]',
    '    A --> P[Cloud Gaming & AR/VR]',
    '    A --> Q[Private 5G for Factories]',
    '    A --> R[Artificial Intelligence]',
    '    R --> S[AI RAN Energy Saving]',
    '    A --> T[Digital Twins]',
    '    A --> U[Satellite Direct-to-Device]',
    '    A -.->|evolves into| V[6G - Future]',
    '    classDef box fill:#EAF2FB,stroke:#1F3864,color:#000;',
    '    class A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V box;',
]
B.append(codeblock(mermaid))
B.append(para(
    'The vertical diagram matches the explanation above: solid arrows show technologies that 5G enables '
    'or depends on, while dashed arrows show what it replaces or what it will become.', sz=20))
B.append(pagebreak())



# ================= 5. POLITICAL AND SOCIAL FACTORS =================
B.append(heading('Political and Social Factors', 1))
B.append(para(
    'Like any emerging technology, 5G depends heavily on outside political and social forces. These '
    'forces can speed up adoption or create real barriers, and they decide how fairly the benefits reach '
    'ordinary people and businesses.', indent=True))
B.append(heading('Political and Regulatory Factors', 2))
B.append(para(
    'In Uzbekistan the government strongly supports faster networks through the \u201cDigital Uzbekistan \u2013 '
    '2030\u201d strategy, which makes digital infrastructure one of its five main pillars and aims to turn the '
    'country into a regional IT hub (OECD, 2026). To manage the sector fairly, in 2025 the government '
    'created a dedicated Telecommunications Regulatory Agency through Law ZRU-1015, which improves '
    'licensing and competition (Legal500, 2025). A presidential decree also gave all licensed operators '
    'direct access to international bandwidth, removing an old monopoly bottleneck (TS2 Tech, 2026). On '
    'the global level there is a political split: the United States and parts of Europe have restricted '
    'Huawei and ZTE for security reasons, which forces countries to choose between cheaper Chinese vendors '
    'and more expensive Western ones such as Nokia and Ericsson. Uzbekistan currently works with both '
    'sides, using ZTE with Ucell and Nokia with Perfectum.', indent=True))



B.append(heading('Social and Cultural Factors', 2))
B.append(para(
    'The biggest social benefit of 5G is digital inclusion. Faster and cheaper mobile internet gives '
    'people in remote regions of Uzbekistan access to online education, e-government and digital health '
    'services that were hard to reach before. 5G also creates new jobs: the regional mobile ecosystem '
    'already supported about 750,000 jobs in 2025, and demand is rising for network engineers, cloud and '
    'edge developers, and cybersecurity specialists (GSMA, 2026). VEON\u2019s \u201cBuildX\u201d software accelerator '
    'in Tashkent is a clear local example of this job creation (VEON, 2026).', indent=True))
B.append(para(
    'There are social risks too. As more devices connect through 5G and IoT, far more personal data is '
    'collected, which raises privacy and surveillance concerns. Uzbekistan responded with its first '
    'AI-focused amendments to information laws in January 2026, adding liability for the unlawful '
    'processing of personal data using AI (Dentons, 2026). Another worry is the digital divide: because '
    '5G first appears in Tashkent and large cities, rural areas could be left behind. Finally, automation '
    'powered by 5G may reduce some routine jobs even while it creates skilled ones, so workers will need '
    'retraining.', indent=True))
B.append(heading('Ecosystem Stakeholders and National Impact', 2))
B.append(para(
    'The political and social environment links many stakeholders together. The government and regulator '
    'set the rules, operators such as Ucell, Beeline and Perfectum build the network, vendors such as ZTE '
    'and Nokia supply the equipment, and businesses and citizens use the services. When these groups work '
    'together, they lower costs, support e-commerce and push the national digital transformation forward.',
    indent=True))



B.append(heading('PEST Analysis Summary Table', 2))
B.append(para(
    'The table below rates the main external factors affecting 5G in Uzbekistan. The weights add up to '
    'exactly 1.00, and each score is the weight multiplied by a strength rating from 1 to 5.', sz=20))
pest = [
    ['Category / Factor', 'Weight (A)', 'Strength (B)', 'Score (A\u00d7B)', 'Type', 'Local Context Comment'],
    ['Political 1. "Digital Uzbekistan \u2013 2030" strategy', '0.15', '5.0', '0.75', '+',
     'Strong state support for digital infrastructure.'],
    ['Political 2. Telecom Regulatory Agency (ZRU-1015) & spectrum policy', '0.15', '4.0', '0.60', '+',
     'Clear licensing and fairer competition.'],
    ['Economic 3. Fast telecom growth (~12.7%/yr, 5G-driven)', '0.15', '4.5', '0.675', '+',
     'Fastest-growing CIS market attracts investment.'],
    ['Economic 4. High CapEx and device cost', '0.10', '3.0', '0.30', '\u2013',
     'Slows rural rollout and mass adoption.'],
    ['Social 5. Digital inclusion and new jobs', '0.15', '4.0', '0.60', '+',
     'Better rural access; new ICT employment.'],
    ['Social 6. Privacy and data-leak risk', '0.10', '4.0', '0.40', '\u2013',
     'More IoT data; addressed by 2026 AI law.'],
    ['Technological 7. Vendor ecosystem & energy efficiency', '0.10', '4.5', '0.45', '+',
     'ZTE green network raised efficiency by 10.6%.'],
    ['Technological 8. Geopolitical vendor restrictions', '0.10', '3.0', '0.30', '\u2013',
     'China vs West vendor split adds risk.'],
    ['Total', '1.00', '', '4.075', '',
     'External environment strongly favours 5G.'],
]
B.append(table(pest, [2700, 900, 1000, 900, 700, 3160]))



B.append(para())
B.append(heading('Interpretation of the PEST Results', 2))
B.append(para(
    'Factors to monitor most closely. The "Digital Uzbekistan \u2013 2030" strategy (0.75) and the fast '
    'market growth (0.675) score highest, so operators must keep their plans aligned with government '
    'programmes and be ready for rapid demand.', indent=True))
B.append(para(
    'Opportunities to use now. The high social demand for digital inclusion and the strong vendor '
    'ecosystem can be turned into private 5G deals for factories and better rural coverage, capturing '
    'market share quickly.', indent=True))
B.append(para(
    'Risks to fix first. High CapEx (0.30) and privacy concerns (0.40) are the main barriers. Operators '
    'should share infrastructure to lower costs and invest in strong security and clear data rules so '
    'that users trust the network. Overall the total score of 4.075 out of 5 shows the external '
    'environment in Uzbekistan strongly favours 5G.', indent=True))
B.append(para())
B.append(para(
    'The stakeholder diagram below (export as a portrait PNG with a white background and dark lines) '
    'summarises how these political and social factors connect.', italic=True, sz=20))
stake = [
    '%%{init: {"theme":"neutral"}}%%',
    'graph TB',
    '    A[5G Deployment in Uzbekistan]',
    '    A --> B[Political Factors]',
    '    A --> C[Social Factors]',
    '    B --> D[Digital Uzbekistan 2030]',
    '    B --> E[Telecom Regulatory Agency]',
    '    B --> F[Spectrum & Vendor Policy]',
    '    C --> G[Digital Inclusion]',
    '    C --> H[New ICT Jobs]',
    '    C --> I[Privacy & Data Risk]',
    '    C --> J[Digital Divide: Urban vs Rural]',
    '    D --> K[Government Investment]',
    '    E --> L[Fair Competition]',
    '    H --> M[Positive: Economic Growth]',
    '    I --> N[Negative: Surveillance Risk]',
    '    J --> O[Challenge: Equal Access]',
    '    classDef box fill:#EAF2FB,stroke:#1F3864,color:#000;',
    '    class A,B,C,D,E,F,G,H,I,J,K,L,M,N,O box;',
]
B.append(codeblock(stake))
B.append(pagebreak())



# ================= 6. CONCLUSION =================
B.append(heading('Conclusion \u2013 Future Impact', 1))
B.append(para(
    'In my opinion, 5G will keep growing strongly in Uzbekistan and will not fail. The main argument is '
    'the clear government support through the "Digital Uzbekistan \u2013 2030" strategy, plus a fast-growing '
    'telecom market and real deployments by Ucell, Beeline and Perfectum. Faster, low-latency '
    'connectivity is simply needed for the smart factories, e-government and digital services the country '
    'wants. However, real risks remain. The high cost of building the network could slow rural coverage '
    'and deepen the digital divide, geopolitical tension over equipment vendors could complicate '
    'partnerships, and the country still needs more trained engineers. Overall, I strongly believe 5G '
    'will succeed in Uzbekistan, but only if the government balances city deployment with rural inclusion '
    'and invests equally in people and infrastructure.', indent=True))

# ================= 7. PRESENTATION =================
B.append(heading('Presentation', 1))
B.append(para(
    'A supporting presentation of 5\u20136 slides covers the key points of this report: the concept of '
    'emerging technology and why 5G fits, how 5G works, the economic factors and local market, the '
    'technology-connections diagram, the political and social factors with the PEST results, and the '
    'conclusion.', indent=True))
B.append(para('Presentation link: [paste your Google Slides / PowerPoint share link here]', sz=20))
B.append(pagebreak())



# ================= 8. REFERENCE LIST =================
def ref(text):
    ppr = ('<w:pPr><w:ind w:left="480" w:hanging="480"/>'
           '<w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr>')
    return f'<w:p>{ppr}{run(text, sz=20)}</w:p>'

B.append(heading('Reference List', 1))
REFS = [
 'CB Insights (2026) Ucell \u2013 Products, Competitors, Financials. Available at: '
 'https://www.cbinsights.com/company/ucell (Accessed: 1 June 2026).',
 'Dentons (2026) Uzbekistan adopts first AI-focused amendments to information and administrative laws. '
 'Available at: https://www.dentons.com/en/insights/articles/2026/january/29/uzbekistan-adopts-first-ai-'
 'focused-amendments-to-information-and-administrative-laws (Accessed: 1 June 2026).',
 'DialAnyone (2026) Ucell mobile data rates in Uzbekistan. Available at: '
 'https://www.dialanyone.com/esim/uzbekistan/ucell (Accessed: 1 June 2026).',
 'Euronews (2025) Uzbekistan launches tax-free zone for major AI and data centre projects. Available at: '
 'https://www.euronews.com/next/2025/11/18/uzbekistan-launches-tax-free-zone-for-major-ai-and-data-'
 'centre-projects-to-attract-investo (Accessed: 1 June 2026).',
 'Fortune Business Insights (2026) 5G Infrastructure Market Size, Share. Available at: '
 'https://www.fortunebusinessinsights.com/index.php/industry-reports/5g-infrastructure-market-100869 '
 '(Accessed: 1 June 2026).',
 'GlobeNewswire (2026) Global Private 5G Network Market to Reach USD 312.2 Billion by 2035. Available at: '
 'https://www.globenewswire.com/news-release/2026/05/21/3299748/0/en/ (Accessed: 1 June 2026).',
 'GSMA (2026) Mobile telecoms accounted for 8% of Eurasia GDP in 2025. Telecompaper. Available at: '
 'https://www.telecompaper.com/news/gsma-says-mobile-telecoms-accounted-for-8-of-eurasia-gdp-in-2025--'
 '1571706 (Accessed: 1 June 2026).',
 'GSMA Intelligence (2026) The Mobile Economy Eurasia 2026. Available at: '
 'https://www.gsmaintelligence.com/research/the-mobile-economy-eurasia-2026 (Accessed: 1 June 2026).',
]
for r in REFS:
    B.append(ref(r))



REFS2 = [
 'Kursiv Media (2025a) Mobile Internet Speeds Up: Beeline Uzbekistan Deploys Innovative Technologies. '
 'Available at: https://uz.kursiv.media/en/2025-05-19/mobile-internet-speeds-up-beeline-uzbekistan-'
 'deploys-innovative-technologies-to-enhance-network-quality/ (Accessed: 1 June 2026).',
 'Kursiv Media (2025b) Uzbekistan Leads CIS in Telecom Industry Growth. Available at: '
 'https://uz.kursiv.media/en/2025-07-01/uzbekistan-leads-cis-in-telecom-industry-growth/ '
 '(Accessed: 1 June 2026).',
 'Legal500 (2025) Telecommunications Regulatory Agency established. Available at: '
 'https://www.legal500.com/developments/press-releases/telecommunications-regulatory-agency-established/ '
 '(Accessed: 1 June 2026).',
 'Mordor Intelligence (2025) Uzbekistan Telecom MNO Market Size, Share, 2025-2030 Outlook. Available at: '
 'https://www.mordorintelligence.com/industry-reports/uzbekistan-telecom-mno-market (Accessed: 1 June 2026).',
 'OECD (2026) Digital Uzbekistan 2030. Available at: '
 'https://oecd.ai/en/dashboards/policy-initiatives/digital-uzbekistan-2030-3968 (Accessed: 1 June 2026).',
 'Ookla (2025) Uzbekistan Speedtest Connectivity Report H1 2025. Available at: '
 'https://www.ookla.com/research/reports/uzbekistan-speedtest-connectivity-report-h1-2025 '
 '(Accessed: 1 June 2026).',
 'Schwab, K. (2016) The Fourth Industrial Revolution. Geneva: World Economic Forum.',
 'Times of Central Asia (2024) Perfectum, Nokia to Launch 5G Network in Uzbekistan. Available at: '
 'https://timesca.com/perfectum-nokia-to-launch-5g-network-in-uzbekistan/ (Accessed: 1 June 2026).',
 'Times of Central Asia (2026) Uzbekistan AI and 5G Push in Focus at GSMA M360 Eurasia. Available at: '
 'https://timesca.com/uzbekistan-ai-and-5g-gsma-m360-eurasia/ (Accessed: 1 June 2026).',
 'TS2 Tech (2026) Uzbekistan\u2019s Internet Makeover: Blazing Speeds, New Satellites, and Lingering Barriers. '
 'Available at: https://ts2.tech/en/uzbekistans-internet-makeover-blazing-speeds-new-satellites-and-'
 'lingering-barriers/ (Accessed: 1 June 2026).',
 'VEON (2026) VEON Unveils the New Beeline Uzbekistan Network Operations Center, Launches BuildX. '
 'Available at: https://www.veon.com/newsroom/press-releases/veon-unveils-the-new-beeline-uzbekistan-'
 'network-operations-center-launches-buildx-to-accelerate-software-development-in-uzbekistan '
 '(Accessed: 1 June 2026).',
 'WHO (2020) Radiation: 5G mobile networks and health. Available at: '
 'https://www.who.int/news-room/questions-and-answers/item/radiation-5g-mobile-networks-and-health '
 '(Accessed: 1 June 2026).',
 'ZTE (2026) Ucell and ZTE Complete Large-Scale Deployment of AI-Powered Green Network Solution in '
 'Uzbekistan. Available at: https://www.zte.com.cn/content/zte-site/www-zte-com-cn/global/about/news/'
 'Ucell-and-ZTE-Complete-Large-Scale-Deployment-of-AI-Powered-Green-Network-Solution-in-Uzbekistan.html '
 '(Accessed: 1 June 2026).',
]
for r in REFS2:
    B.append(ref(r))



# ================= ASSEMBLE & PACKAGE =================
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
body_xml = ''.join(B)
document = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:document {NS}><w:body>{body_xml}'
    '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" '
    'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr></w:body></w:document>')

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-'
    'officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-'
    'officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-'
    'officedocument.wordprocessingml.numbering+xml"/></Types>')

rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
    'relationships/officeDocument" Target="word/document.xml"/></Relationships>')

word_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
    'relationships/styles" Target="styles.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
    'relationships/numbering" Target="numbering.xml"/></Relationships>')



styles = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:styles xmlns:w="{W}">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
    '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
    '<w:sz w:val="22"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>'
    '<w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
    '<w:pPr><w:outlineLvl w:val="0"/></w:pPr>'
    '<w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>'
    '<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>'
    '<w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/>'
    '<w:pPr><w:outlineLvl w:val="1"/></w:pPr>'
    '<w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style></w:styles>')

numbering = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:numbering xmlns:w="{W}">'
    '<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0">'
    '<w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="\u2022"/>'
    '<w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>'
    '<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/></w:rPr>'
    '</w:lvl></w:abstractNum>'
    '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num></w:numbering>')

out_path = '/projects/sandbox/new_ai/5G_Emerging_Technology_Assignment.docx'
with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', content_types)
    z.writestr('_rels/.rels', rels)
    z.writestr('word/_rels/document.xml.rels', word_rels)
    z.writestr('word/document.xml', document)
    z.writestr('word/styles.xml', styles)
    z.writestr('word/numbering.xml', numbering)

print('SUCCESS:', out_path)
print('Size:', os.path.getsize(out_path), 'bytes')
print('Body parts:', len(B))
