import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
np.random.seed(42)

print("="*60)
print("FEATURE ENGINEERING - Sozdanie priznakov")
print("="*60)

print("\nSozdaem bazovye dannye...")

n = 200 

data = {
    'ploshchad' : np.random.randit(30, 150, n),
    'komnat': np.random.randint(1, 5, n),
    'etazh': np.random.randint(1, 20, n),
    'god_postroyki': np.random.randint(1980, 2024, n),
    'rasstoyanie_tsentr': np.random.uniform(1, 30, n)
    }

df = pd.DataFrame(data) 

tsena = (
    df['ploshchad'] * 100 + 
     df['komnat'] * 5000 +
    (df['ploshchad'] / df['komnat']) * 500 +  # ploshchad na komnatu!
    (2024 - df['god_postroyki']) * (-200) +   # vozrast doma
    df['rasstoyanie_tsentr'] * (-300) +
    np.random.normal(0, 2000, n)
)

df['tsena'] = tsena

print(f"\nSozdano {len(df)} kvartir")
print("\nPervye stroki:")
print(df.head())

print("\n" + "="*60)
print("SPOSOB 1: Prostye kombinatsii")
print("="*60)

# 1. Delenie
df['ploshchad_na_komnatu'] = df['ploshchad'] / df['komnat']
"""
Delenie - ochen poleznaya operatsiya

Ploshchad_na_komnatu pokazyvaet:
100m² / 2 komnaty = 50m² na komnatu (prostorno!)
100m² / 5 komnat = 20m² na komnatu (tesno)

Kvartira s bolshoy ploshchadyu na komnatu dorozhe!
"""

# 2. Umnozhenie
df['ploshchad_x_komnat'] = df['ploshchad'] * df['komnat']
"""
Umnozhenie - vzaimodeystvie

Bolshaya ploshchad I mnogo komnat = ochen dorogo!
Malenkaya ploshchad I malo komnat = deshevo
"""

# 3. Raznost
df['vozrast_doma'] = 2024 - df['god_postroyki']
"""
Preobrazovanie chisla v ponytnyy priznak

God 2020 → Vozrast 4 goda
God 1990 → Vozrast 34 goda

Modeli legche rabotat s vozrastom!
"""

# 4. Summa
df['obshchaya_kharakteristika'] = df['ploshchad'] + df['komnat'] + df['etazh']
"""
Summa mozhet byt poleznoy kogda:
Vse priznaki vnesyat vklad v obshchuyu kharakteristiku
"""

print("\nNovye priznaki sozdany:")
print("  1. ploshchad_na_komnatu (delenie)")
print("  2. ploshchad_x_komnat (umnozhenie)")
print("  3. vozrast_doma (raznost)")
print("  4. obshchaya_kharakteristika (summa)")

print("\nPrimery novykh dannykh:")
print(df[['ploshchad', 'komnat', 'ploshchad_na_komnatu']].head())


print("\n" + "="*60)
print("SPOSOB 2: Logarifmicheskaya transformatsiya")
print("="*60)

df['log_ploshchad'] = np.log1p(df['ploshchad'])
df['log_tsena'] = np.log1p(df['tsena'])
"""
log1p(x) = log(1 + x)

ZACHEM NUZHNO:

1. Szhatie bolshikh znacheniy:
   1000 → log(1001) ≈ 6.9
   10000 → log(10001) ≈ 9.2
   Raznitsa umenshilas!

2. Simetrizatsiya raspredeleniya:
   Esli dannye silno skosheny (mnogo malenkikh, malo bolshikh)
   Log delaet raspredelenie bolee normalnym

3. Linearizatsiya zavisimostey:
   Esli zavisimost eksponentsialnaya: y = e^x
   Log(y) = x → lineynaya zavisimost!

KOGDA ISPOLZOVAT:
- Silno raznye masshtaby (1 do 1000000)
- Skoshennoe raspredelenie
- Eksponentsialnye zavisimosti
"""

print("\nLog transformatsiya:")
print(f"  Ploshchad: min={df['ploshchad'].min()}, max={df['ploshchad'].max()}")
print(f"  Log ploshchad: min={df['log_ploshchad'].min():.2f}, max={df['log_ploshchad'].max():.2f}")


print("\n" + "="*60)
print("SPOSOB 3: Stepenye priznaki")
print("="*60)

df['ploshchad_kvadrat'] = df['ploshchad'] ** 2
df['ploshchad_kub'] = df['ploshchad'] ** 3
"""
Stepen priznaka nuzhen kogda:
Zavisimost ne lineynaya!

Primer:
Tsena mozhet rasti ne prosto s ploshchadyu,
a s KVADRATOM ploshchadi!

Ploshchad 50m² → Tsena 5 mln
Ploshchad 100m² → Tsena ne 10 mln, a 20 mln! (kvadratichnaya zavisimost)

X² - kvadrat (chasto pomogaet)
X³ - kub (redko, dlya silno nelineynykh zavisimostey)
"""

print("\nStepenye priznaki:")
print(f"  Ploshchad: {df['ploshchad'].iloc[0]}")
print(f"  Kvadrat: {df['ploshchad_kvadrat'].iloc[0]}")
print(f"  Kub: {df['ploshchad_kub'].iloc[0]}")

# ============================================
# SPOSOB 4: BINARNYE PRIZNAKI
# ============================================

print("\n" + "="*60)
print("SPOSOB 4: Binarnye priznaki")
print("="*60)

df['bolshaya_kvartira'] = (df['ploshchad'] > 80).astype(int)
df['novostroyka'] = (df['vozrast_doma'] <= 5).astype(int)
df['vysokiy_etazh'] = (df['etazh'] > 10).astype(int)
"""
Binarnye priznaki: 0 ili 1 (da/net)

(uslovie).astype(int) - prevrashchaet True/False v 1/0

ZACHEM:
Inogda kategoriya vazhnee tochnogo chisla!

Primer:
Vozrast 3 goda vs 4 goda - ne ochen vazhno
No "Novostroyka (da/net)" - ochen vazhno!

KOGDA ISPOLZOVAT:
- Est znachimye porogi (>10 etazh = vysokiy)
- Kategorii vazhnee chisel
"""

print("\nBinarnye priznaki:")
print(f"  Bolshikh kvartir (>80m²): {df['bolshaya_kvartira'].sum()}")
print(f"  Novostroek (≤5 let): {df['novostroyka'].sum()}")
print(f"  Vysokikh etazhey (>10): {df['vysokiy_etazh'].sum()}")

# ============================================
# SPOSOB 5: GRUPPOVYE PRIZNAKI
# ============================================

print("\n" + "="*60)
print("SPOSOB 5: Gruppovye priznaki")
print("="*60)

# Razbit na gruppy
df['kategoriya_ploshchadi'] = pd.cut(
    df['ploshchad'],
    bins=[0, 50, 80, 120, 200],
    labels=['Malenkaya', 'Srednyaya', 'Bolshaya', 'Ochen_bolshaya']
)
"""
pd.cut() - razbit chislo na intervaly (kategoriyi)

bins - granitsy intervalov
labels - nazvaniya grupp

Primer:
35m² → попадает в [0, 50] → 'Malenkaya'
75m² → попадает в [50, 80] → 'Srednyaya'
100m² → попадает в [80, 120] → 'Bolshaya'

ZACHEM:
Model mozhet uchit razlichiya mezhdu gruppami
vmesto tochnykh chisel
"""

print("\nRaspredelenie po kategoriyam:")
print(df['kategoriya_ploshchadi'].value_counts())

# ============================================
# SRAVNENIE: DO I POSLE
# ============================================

print("\n" + "="*60)
print("SRAVNENIE: skolko priznakov")
print("="*60)

bazovye = ['ploshchad', 'komnat', 'etazh', 'god_postroyki', 'rasstoyanie_tsentr']
novye = [
    'ploshchad_na_komnatu', 'ploshchad_x_komnat', 'vozrast_doma',
    'obshchaya_kharakteristika', 'log_ploshchad', 'log_tsena',
    'ploshchad_kvadrat', 'ploshchad_kub', 'bolshaya_kvartira',
    'novostroyka', 'vysokiy_etazh'
]

print(f"\nBazovykh priznakov: {len(bazovye)}")
print(f"Novykh priznakov: {len(novye)}")
print(f"Vsego: {len(bazovye) + len(novye)}")

# ============================================
# VIZUALIZATSIYA
# ============================================

print("\nVizualiziruem novye priznaki...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Graf 1: Ploshchad na komnatu vs Tsena
axes[0, 0].scatter(df['ploshchad_na_komnatu'], df['tsena'], 
                   alpha=0.5, s=30)
axes[0, 0].set_title('Ploshchad na komnatu vs Tsena', fontweight='bold')
axes[0, 0].set_xlabel('Ploshchad na komnatu (m²)')
axes[0, 0].set_ylabel('Tsena')
axes[0, 0].grid(True, alpha=0.3)

# Graf 2: Vozrast doma vs Tsena
axes[0, 1].scatter(df['vozrast_doma'], df['tsena'], 
                   alpha=0.5, s=30, color='coral')
axes[0, 1].set_title('Vozrast doma vs Tsena', fontweight='bold')
axes[0, 1].set_xlabel('Vozrast doma (let)')
axes[0, 1].set_ylabel('Tsena')
axes[0, 1].grid(True, alpha=0.3)

# Graf 3: Binarnye priznaki
binary_features = ['bolshaya_kvartira', 'novostroyka', 'vysokiy_etazh']
counts = [df[feat].sum() for feat in binary_features]
axes[1, 0].bar(range(len(binary_features)), counts, color='skyblue')
axes[1, 0].set_xticks(range(len(binary_features)))
axes[1, 0].set_xticklabels(['Bolshaya\nkvartira', 'Novostroyka', 
                            'Vysokiy\netazh'], rotation=0)
axes[1, 0].set_title('Binarnye priznaki', fontweight='bold')
axes[1, 0].set_ylabel('Kolichestvo')
axes[1, 0].grid(True, alpha=0.3, axis='y')

# Graf 4: Raspredelenie po kategoriyam
kategory_counts = df['kategoriya_ploshchadi'].value_counts()
axes[1, 1].bar(range(len(kategory_counts)), kategory_counts.values, 
               color='green', alpha=0.7)
axes[1, 1].set_xticks(range(len(kategory_counts)))
axes[1, 1].set_xticklabels(kategory_counts.index, rotation=45, ha='right')
axes[1, 1].set_title('Kategorii ploshchadi', fontweight='bold')
axes[1, 1].set_ylabel('Kolichestvo')
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.show()

# ============================================
# REZYUME
# ============================================

print("\n" + "="*60)
print("REZYUME:")
print("="*60)

print("""
SOZDALI 5 TIPOV PRIZNAKOV:

1. KOMBINATSII (/, *, +, -)
   - ploshchad / komnat
   - ploshchad * komnat

2. LOGARIFMY
   - log(ploshchad)
   - Szhimaet bolshie znacheniya

3. STEPENI
   - ploshchad²
   - ploshchad³

4. BINARNYE (0/1)
   - bolshaya_kvartira
   - novostroyka

5. GRUPPY (kategorii)
   - Malenkaya/Srednyaya/Bolshaya

GLAVNOE:
Novye priznaki dayut modeli NOVUYU INFORMATSIYU!
""")

print("\n Sozdanie priznakov osvoeno!")
print("="*60)
