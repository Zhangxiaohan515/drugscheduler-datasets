# Consumer Group Mapping — Rules & Assignment (v4, aligned to 12 goals, headline-first products)
## Structure
Raw ingredient → canonical ingredient (ING_ID) → **consumer group** (53 network nodes) → **primary goal** (one of 12; used to color nodes) + **secondary goals** (overlaps).
Every consumer group sits under exactly one primary goal, so nodes can be colored or clustered by goal directly. Secondary goals are set at group level and show where groups overlap.
## Rules

**Rule 0 — Exclude non-actives.** Excipients, sweeteners, capsule materials, absorption enhancers and counter-ions map to EXCLUDE and never enter the network.

**Rule 1 — Forms collapse to the parent nutrient.** Salts, chelates, isomers and vitamers go to the parent (Mg glycinate/threonate → Magnesium; methylcobalamin → B12; MK-7/K1 → Vitamin K; every probiotic strain → Probiotics).

**Rule 2 — Products count toward what their name advertises (v4, product level).** A product is one consumer decision. Its ingredients are first mapped to groups (Rules 0–1, 3–4); then, in order:
1. *One group* → that group.
2. *Name says multivitamin* (multivitamin, multimineral, multiple vitamins, prenatal, one-a-day, Opti-Men …) → **Multivitamin** only; lutein, lycopene, choline, inositol, fruit powders etc. inside it are not counted separately. An anchor product named alongside it (e.g. "Multivitamin + Omega-3") is kept.
3. *Name advertises groups* → only those groups. Specific words select one group ("Vitamin D3 + K2" → Vitamin D and Vitamin K; "Krill Oil" → Omega-3; "Gold Standard Whey" → Protein; "B-50 Complex" → B Complex). Generic goal words select every present group serving that goal ("Sleep Gummies" → Sleep & Calm and Melatonin; "Eye Vital" → Eye Health; "Pre-Workout" → Caffeine, Amino Acids, Brain Health).
4. *Unnamed formula with ≥3 vitamins/minerals* → the multi-first rule below, and the whole product becomes Multivitamin (or B Complex).
5. *Any other unnamed formula* → every group with an active ingredient; carrier/companion ingredients (choline, inositol, PABA, lecithin/phospholipids, vitamin E tocopherols, threonate) are not counted.

The keyword lists live in `build_mapping_v4.py` (`HEADLINE_KEYWORDS`, `GOAL_KEYWORDS`, `MULTI_TITLE`) and are copied into `consumer_group_rules_v4.json`. Every dropped group is listed per product in `ingredient_groups_not_counted`.

Why: in v3 every ingredient of every product counted, so 101 users reached Eye Health only through the lutein in a multivitamin, 120 reached Women's Health through the inositol in B-50/B-100 tablets, and 177 reached Brain Health through their choline. `mapping_v3_vs_v4_prevalence.csv` in the statistics folder lists the change for every group.

**Rule 2a — Multi-first for vitamins & minerals.** Used in step 4 above:
- ≥3 vitamins/minerals → **Multivitamin** (covers multiminerals);
- if B vitamins are ≥4 of them and ≥ half the vitamin/mineral content → **B Complex** instead;
- otherwise each maps individually (D3 + K2 → Vitamin D and Vitamin K; ZMA → Zinc, Magnesium, B Complex).
Multivitamin has no ING_ID; it is assigned from product composition.
Sodium fluoride (ING-633) counts as fluoride, one distinct mineral; it is not a standalone sodium entry.

**Rule 3 — Famous ingredients keep their own node; the rest roll up to a family.** Own nodes: Magnesium, Zinc, Iron, Calcium, Vitamin D/C/K, B12, Folate, Biotin, Creatine, Collagen, Melatonin, Ashwagandha, Curcumin, NAC, CoQ10, Caffeine.

**Rule 4 — Assign by main consumer use, not chemistry.** One ingredient → one group. E.g., Calcium D-Glucarate → Liver Support; Ca-AKG → NAD+; Zinc-Carnosine → Gut Health; Choline → Brain Health; Semax/Selank → Nootropics.

**Rule 5 — Groups are cut to fit the 12 goals.** A group never straddles two primary goals. Where a v1 group was mixed, it was split or its members re-homed by goal:
- Eye Health split out of Antioxidants (Lutein, Zeaxanthin, Bilberry, Marigold, Eyebright, Mingmu Dihuang Wan).
- Old "Other Meds" and "Hormones" dissolved: cardio-metabolic drugs + thyroid → **Metabolic Meds**; TRT, Enclomiphene, anabolics, Finasteride, Minoxidil, Tadalafil → **Men's Rx**; DHEA / 7-Keto / Pregnenolone → Men's Health; HRT and birth control → Women's Health; GI drugs → Gut Health; antihistamines, cough medicine, PrEP → Immune Support; Psilocybin, Kratom → Mental Health Meds.
- Peptides: cognitive peptides (Semax, Selank, Cerebrolysin) → Nootropics; MOTS-c, SS-31 → CoQ10; the rest (BPC-157, TB-500, GH secretagogues, etc.) stay in Peptides under Sleep and Recovery.

**Rule 6 — Medication nodes.** Six nodes are pure medication nodes: GLP-1, Metabolic Meds, ADHD Meds, Mental Health Meds, Men's Rx, Peptides. Smaller drug classes are folded into the supplement node of their goal (Women's Health, Gut Health, Immune Support); `is_drug = 1` is kept at ingredient level so drug use can still be counted.

**Rule 7 — Wider-than-name groups.** Omega-3 includes other dietary oils & fats (MCT, flax, omega-6/9). NAD+ includes longevity compounds (NMN, NR, Resveratrol, Spermidine, Urolithin A, Fisetin, TMG, Ca-AKG). CoQ10 includes mitochondrial support (PQQ, Carnitine, ALA, Methylene Blue, MOTS-c, SS-31). NAC includes glutathione. Sleep & Calm includes mood support. Blood Sugar includes weight management. Caffeine includes other stimulants. Greens includes fruit/veg powders and superfoods. Collagen includes hair/skin/nail ingredients. Adaptogens includes TCM tonic herbs. Beef Organs includes glandulars and oyster.

**Rule 8 — Counting.** A user counts once per group (and once per goal), however many ingredients they take from it.

**Rule 9 — Small groups.** If a group has very few users (e.g., <0.5%), merge it into the closest node under the same goal before drawing.
## Goal → consumer groups
| Goal | Groups (primary) | Also related (secondary) |
|---|---|---|
| General Health | Multivitamin, B Complex, B12, Folate, Vitamin D, Vitamin A & E, Magnesium, Iron, Electrolytes, Trace Minerals, Omega-3, Greens, Beef Organs | — |
| Sleep and Recovery | Melatonin, Sleep & Calm, Ashwagandha, Adaptogens, Mental Health Meds, Peptides | Magnesium, Amino Acids |
| Bone and Joint Health | Calcium, Vitamin K, Joint Support, Curcumin | Vitamin D, Trace Minerals, Collagen |
| Longevity and Anti-aging | NAD+, CoQ10, NAC, Antioxidants | Peptides, Curcumin, Mushrooms, Heart Health, Men's Health |
| Immune Support | Vitamin C, Zinc, Mushrooms, Immune Support | Vitamin D, NAC, Probiotics |
| Skin, Hair and Nails | Biotin, Collagen | Vitamin A & E, Peptides, Joint Support, Antioxidants, Vitamin C, Zinc, Men's Rx |
| Performance and Cognition | Protein, Creatine, Amino Acids, Brain Health, Nootropics, Caffeine, ADHD Meds | B Complex, B12, Magnesium, Electrolytes, Omega-3, Ashwagandha, Adaptogens, Peptides, CoQ10, Mushrooms |
| Gut and Digestion | Probiotics, Fiber, Digestive Enzymes, Gut Health, Liver Support | Greens |
| Eye and Vision Health | Eye Health | Vitamin A & E, Omega-3 |
| Metabolic Health | Blood Sugar, Heart Health, GLP-1, Metabolic Meds | Trace Minerals, Omega-3, Vitamin K, NAD+, CoQ10, Fiber, Liver Support |
| Women's Health | Women's Health | Folate, Iron, Calcium |
| Men's Health | Men's Health, Men's Rx | Beef Organs, Ashwagandha, Zinc |

## Assignment by goal and group

### General Health

**Multivitamin** — assigned at product level (Rule 2); no direct ING_ID.

**B Complex** (11) · also: Performance and Cognition
- ING-003 P-5-P, Vitamin B6
- ING-004 Thiamin, Vitamin B1
- ING-005 Riboflavin, Vitamin B2
- ING-006 Niacin, Vitamin B3
- ING-008 Pantothenic acid, Vitamin B5
- ING-093 pyridoxine HCl, Vitamin B6
- ING-308 Niacinamide / Nicotinamide
- ING-353 Benfotiamine
- ING-742 Para-aminobenzoic acid (PABA)
- ING-1208 Pantethine
- ING-1323 Brewer's yeast — _B-vitamin food source_

**B12** (3) · also: Performance and Cognition
- ING-002 Methylcobalamin, Vitamin B12
- ING-227 Cobalamin, Vitamin B12
- ING-309 Cyanocobalamin, Vitamin B12

**Folate** (3) · also: Women's Health
- ING-001 5-MTHF / Methylfolate
- ING-115 folate
- ING-391 Folic Acid, Vitamin B9 (synthetic)

**Vitamin D** (2) · also: Bone and Joint Health, Immune Support
- ING-010 Cholecalciferol. Vitamin D3
- ING-501 Ergocalciferol, Vitamin D2

**Vitamin A & E** (8) · also: Eye and Vision Health, Skin, Hair and Nails
- ING-013 Retinoids, Vitamin A
- ING-014 d-alpha-tocopherol, Vitamin E
- ING-020 beta-carotene, Vitamin A — _labeled as provitamin A_
- ING-899 Tocopherols
- ING-999 Tocotrienols
- ING-1039 Gamma-Tocopherol
- ING-1219 Delta-Tocopherol
- ING-1220 Beta-Tocopherol

**Magnesium** (11) · also: Sleep and Recovery, Performance and Cognition
- ING-027 Magnesium glycinate
- ING-156 Magnesium citrate
- ING-186 magnesium oxide
- ING-188 magnesium L-Threonate, magtein
- ING-201 Magnesium Malate
- ING-251 threonic acid — _counter-ion from magnesium L-threonate_
- ING-302 Magnesium (unspecified form)
- ING-913 Magnesium Hydroxide
- ING-1045 Magnesium Lysinate Glycinate Chelate
- ING-1046 Magnesium Orotate
- ING-1047 Magnesium Taurate

**Iron** (10) · also: Women's Health
- ING-153 Iron
- ING-635 Ferrous Gluconate
- ING-636 Ferrous Sulfate
- ING-773 Heme Iron
- ING-803 Ferrous Fumarate
- ING-1040 Ferrous Bisglycinate
- ING-1041 Ferric Sodium EDTA
- ING-1042 Ferric Pyrophosphate
- ING-1055 Polysaccharide Iron Complex
- ING-1058 Sucrosomial Iron

**Electrolytes** (5) · also: Performance and Cognition
- ING-032 Sodium
- ING-194 potassium
- ING-284 Sodium minerals (Baja Gold / sea salt)
- ING-737 Sodium Bicarbonate
- ING-1290 Chloride

**Trace Minerals** (18) · also: Bone and Joint Health, Metabolic Health
- ING-029 Selenium
- ING-031 Copper
- ING-033 Manganese
- ING-034 Chromium
- ING-035 Molybdenum
- ING-036 Boron
- ING-037 Iodine
- ING-094 Potassium Iodide — _iodine source_
- ING-095 Vanadium
- ING-154 Phosphorus
- ING-165 Lithium Orotate
- ING-200 Lithium
- ING-494 Silicon
- ING-495 Nickel
- ING-497 Strontium citrate
- ING-1059 Vanadyl Sulfate
- ING-1230 Lithium Citrate
- ING-633 Sodium Fluoride — _Fluoride mineral; counts as one distinct mineral in product-level multi-first rule, not as standalone sodium._

**Omega-3** (13) · also: Metabolic Health, Performance and Cognition, Eye and Vision Health
- ING-016 EPA / Eicosapentaenoic acid
- ING-017 DHA / Docosahexaenoic acid
- ING-018 DPA / Docosapentaenoic acid
- ING-182 Oleic acid / Omega-9 — _Omega-3 node also holds other dietary oils/fats_
- ING-267 MCT / C8 Caprylic acid (Brain Octane) — _MCT oil; Omega-3 node also holds other dietary oils/fats_
- ING-399 Krill Oil
- ING-546 Palmitic Acid — _dietary fat; Omega-3 node also holds other oils/fats_
- ING-685 Linoleic Acid — _omega-6; Omega-3 node also holds other oils/fats_
- ING-804 Arachidonic Acid — _omega-6; Omega-3 node also holds other oils/fats_
- ING-1037 Flaxseed Oil
- ING-1038 Gamma-Linolenic Acid / GLA
- ING-1051 Omega-6 Fatty Acids — _omega-6; Omega-3 node also holds other oils/fats_
- ING-1313 Safflower Oil — _dietary oil; Omega-3 node also holds other oils/fats_

**Greens** (41) · also: Gut and Digestion
- ING-065 Sodium copper chlorophyllin — _chlorophyll, not a copper supplement_
- ING-217 spirulina
- ING-220 chlorella
- ING-312 Apple powder
- ING-313 Carrot powder
- ING-314 Pineapple juice powder
- ING-316 Orange juice powder
- ING-317 Spinach powder
- ING-318 Broccoli powder / extract
- ING-338 Plum powder
- ING-339 Strawberry powder
- ING-340 Cherry powder
- ING-342 Tomato powder
- ING-371 Rose hips powder
- ING-384 acai berry — _superfruit_
- ING-431 Kelp — _sea vegetable_
- ING-440 Fulvic Acid
- ING-502 Organic Fruit & Veggie Blend (Organic Cauliflower, Organic Spinach, Organic Carrot, Organic Beet, Organic Tomato, Organic Blueberry, Organic Cranberry, Organic Cherry, Organic Raspberry and Organic Strawberry)
- ING-1026 Sweet Apricot Kernel Powder
- ING-1034 Cauliflower
- ING-1043 Kale
- ING-1106 Calamansi / Citrus microcarpa
- ING-1109 Goji — _superfruit_
- ING-1112 Irish Sea Moss / Chondrus crispus
- ING-1118 Parsley Leaf
- ING-1223 Basil / Ocimum basilicum
- ING-1224 Brussels Sprouts
- ING-1229 Lemon / Citrus limon
- ING-1235 Pear Powder
- ING-1236 Banana Powder
- ING-1237 Cabbage Powder
- ING-1238 Asparagus Powder
- ING-1239 Cucumber Powder
- ING-1240 Pea Powder
- ING-1297 Prune Powder
- ING-1311 Watercress
- ING-1312 Persimmon
- ING-1315 Morinda Citrifolia
- ING-1316 Coconut
- ING-1326 Food blend
- ING-507 Alfalfa extract — _Alfalfa botanical extract._

**Beef Organs** (16) · also: Men's Health
- ING-127 Oyster Extract Powder — _animal whole-food (zinc source), grouped with organ supplements_
- ING-418 Grass-Fed Organ Complex
- ING-453 Beef Heart
- ING-454 Beef Kidney
- ING-455 Beef Pancreas
- ING-456 Beef Spleen
- ING-480 American Grass-Fed Liver (Bovine)
- ING-528 Bovine bone marrow
- ING-1116 Neonatal Thymus Concentrate (bovine) — _glandular_
- ING-1163 Neonatal Adrenal Complex Concentrate (bovine) — _glandular_
- ING-1164 Orchic Concentrate (bovine) — _glandular_
- ING-1260 Beef Intestine
- ING-1261 Beef Tripe
- ING-1262 Beef Testicle
- ING-1263 Beef Prostate
- ING-1301 Amnion — _glandular_

### Sleep and Recovery

**Melatonin** (1)
- ING-112 Melatonin

**Sleep & Calm** (21)
- ING-111 L-theanine
- ING-146 apigenin
- ING-147 Gamma-Aminobutyric Acid (GABA)
- ING-148 Glycine
- ING-228 L-Tryptophan — _mood/sleep amino acid_
- ING-229 Valerian Root
- ING-386 Chamomile extract
- ING-398 5-HTP — _mood/sleep_
- ING-412 CBD
- ING-423 Lemon Balm
- ING-438 Passionflower
- ING-439 Hops Flower
- ING-538 St John's Wort Extract — _mood_
- ING-539 S-Adenosylmethionine (SAMe) — _mood_
- ING-541 Saffron Extract — _mood_
- ING-1198 Hemp Extract — _with CBD_
- ING-1200 Lavender Oil / Silexan
- ING-1202 Magnolia officinalis Bark Extract
- ING-1203 Phellodendron amurense Bark Extract — _Relora component_
- ING-1264 Honokiol
- ING-1319 American Skullcap (Scutellaria lateriflora)

**Ashwagandha** (1) · also: Performance and Cognition, Men's Health
- ING-151 Ashwagandha Extract

**Adaptogens** (19) · also: Performance and Cognition
- ING-122 Panax Ginseng Extract
- ING-152 Rosavins, Rhodiola Rosea Extract
- ING-401 Maca Root
- ING-417 Gynostemma
- ING-428 Schisandra
- ING-499 Holy Basil / Tulsi
- ING-523 American Ginseng Root Extract Panax quinquefolius
- ING-524 Eleutherococcus senticosus root extract
- ING-1107 Chinese Yam / Dioscorea — _TCM tonic herb_
- ING-1119 Poria cocos — _TCM tonic herb_
- ING-1283 Air potato — _TCM herb_
- ING-1284 Bearded scutellaria — _TCM herb_
- ING-1286 Codonopsis — _TCM tonic herb_
- ING-1288 Peach kernel — _TCM herb_
- ING-1289 Curcuma zedoaria — _TCM herb (zedoary, not turmeric)_
- ING-1308 Greater celandine — _TCM herb_
- ING-1309 Pueraria Montana Var. Lobata Whole — _TCM herb_
- ING-1310 Black nightshade — _TCM herb_
- ING-1325 Dendrobium officinale powder — _TCM tonic herb_

**Mental Health Meds** (10)
- ING-268 Kratom / Mitragyna speciosa — _psychoactive, not Rx_
- ING-534 Sertraline
- ING-556 Alprazolam
- ING-676 Bupropion
- ING-1196 Duloxetine
- ING-1197 Escitalopram
- ING-1199 Hydroxyzine — _prescribed mainly for anxiety_
- ING-1216 Psilocybin — _psychoactive, not Rx_
- ING-1273 Agomelatine
- ING-1274 Lamotrigine

**Peptides** (14) · also: Longevity and Anti-aging, Performance and Cognition, Skin, Hair and Nails
- ING-276 Human Growth Hormone (HGH) — _HGH grouped with GH peptides_
- ING-420 BPC-157
- ING-1136 TB-500
- ING-1152 AOD-9604
- ING-1160 Ipamorelin
- ING-1161 Kisspeptin
- ING-1171 Sermorelin
- ING-1174 Tesamorelin
- ING-1178 GHK-Cu
- ING-1180 Melanotan I / Afamelanotide
- ING-1195 DSIP / Delta Sleep-Inducing Peptide
- ING-1207 KPV
- ING-1276 MK-677 (Ibutamoren) — _GH secretagogue_
- ING-1277 GHRP-6

### Bone and Joint Health

**Calcium** (3) · also: Women's Health
- ING-030 Calcium
- ING-383 Calcium citrate
- ING-654 Calcium Carbonate

**Vitamin K** (3) · also: Metabolic Health
- ING-011 Phytonadione, Vitamin K1
- ING-012 Menaquinone-4, Vitamin K2
- ING-319 Menaquinone-7, Vitamin K2

**Joint Support** (9) · also: Skin, Hair and Nails
- ING-159 Glucosamine Sulfate
- ING-161 Hyaluronic acid / Sodium hyaluronate
- ING-232 Chondroitin sulfate (sodium)
- ING-303 MSM / Methylsulfonylmethane
- ING-344 Undenatured type II collagen
- ING-372 Glucosamine HCl
- ING-441 Boswellia
- ING-487 Palmitoylethanolamide (PEA) — _PEA for pain/inflammation_
- ING-1132 Glucosamine

**Curcumin** (3) · also: Longevity and Anti-aging
- ING-050 Curcumin
- ING-466 Turmeric root extract / Curcuma longa
- ING-1265 Tetrahydrocurcumin

### Longevity and Anti-aging

**NAD+** (13) · also: Metabolic Health
- ING-042 Ergothioneine — _marketed as longevity compound_
- ING-045 NMN / Nicotinamide mononucleotide
- ING-047 Urolithin A / Mitopure — _longevity_
- ING-055 Fisetin — _senolytic / longevity_
- ING-056 Trans-resveratrol — _longevity (resveratrol)_
- ING-155 Niagen / Nicotinamide Riboside
- ING-157 calcium alpha-keto glutarate — _Ca-AKG is a longevity compound, not a calcium supplement_
- ING-164 Spermidine — _longevity_
- ING-199 pterostilbene — _longevity (resveratrol analog)_
- ING-252 TMG / Trimethylglycine / Betaine anhydrous — _commonly stacked with NMN_
- ING-365 NAD+ / Nicotinamide adenine dinucleotide
- ING-1138 5-Amino-1MQ
- ING-1226 Japanese Knotweed / Fallopia japonica — _resveratrol source_

**CoQ10** (10) · also: Metabolic Health, Performance and Cognition
- ING-025 Coenzyme Q10 / Ubiquinone
- ING-026 Ubiquinol
- ING-041 Alpha lipoic acid — _mitochondrial support (CoQ10 group = CoQ10 & mitochondria)_
- ING-196 Pyrroloquinoline Quinone — _mitochondrial support_
- ING-197 Acetyl-L-Carnitine — _mitochondrial support (carnitine)_
- ING-269 Methylene blue — _mitochondrial support_
- ING-359 Adenosine triphosphate (ATP) — _cellular energy_
- ING-781 Carnitine — _mitochondrial support (carnitine)_
- ING-1146 MOTS-C — _mitochondrial peptide_
- ING-1149 SS-31 / Elamipretide — _mitochondrial peptide_

**NAC** (2) · also: Immune Support
- ING-040 NAC / N-Acetyl-L-Cysteine
- ING-160 L-glutathione — _glutathione grouped with NAC_

**Antioxidants** (38) · also: Skin, Hair and Nails
- ING-021 Astaxanthin — _carotenoid_
- ING-024 Lycopene — _carotenoid_
- ING-051 Quercetin
- ING-052 Luteolin
- ING-054 Rutin
- ING-059 Pomegranate ellagitannins
- ING-096 Mixed carotenoids — _carotenoid_
- ING-104 PowerGrape grape / Vitis vinifera
- ING-105 Superfruit antioxidant blend
- ING-106 Green tea extract / Camellia sinensis
- ING-166 Grape seed extract Polyphenols
- ING-167 Pomegranate Juice Extract Polyphenols
- ING-175 Cocoa flavanols
- ING-253 Sulforaphane / BroccoMax
- ING-335 Blueberry extract / powder
- ING-337 Raspberry extract
- ING-367 Myrosinase — _sulforaphane activator_
- ING-387 Pycnogenol extract
- ING-392 Citrus Bioflavonoid Complex
- ING-525 Olive extract
- ING-608 Naringin
- ING-684 Grapefruit Extract
- ING-705 Polyphenols
- ING-1099 Amla / Phyllanthus emblica
- ING-1117 Orange Peel Extract
- ING-1139 Catalase
- ING-1140 Cyanidin-3-glucoside
- ING-1142 French Melon Concentrate — _SOD source_
- ING-1143 Glucoraphanin
- ING-1144 Grape Skin Extract
- ING-1148 Sesamin
- ING-1150 Superoxide Dismutase
- ING-1183 Rose Extract
- ING-1186 Cocoa Mass — _cocoa_
- ING-1232 Oligomeric Procyanidins / OPCs
- ING-1233 Alpha-Carotene — _carotenoid_
- ING-1147 Oligonol — _Lychee-derived polyphenols._
- ING-1270 Theaflavins — _Black-tea polyphenols. Metabolic Health is a possible ingredient-specific secondary association, not encoded by the current group-level secondary-goal schema._

### Immune Support

**Vitamin C** (3) · also: Skin, Hair and Nails
- ING-038 Ascorbic acid, Vitamin C
- ING-247 Calcium Ascorbate
- ING-385 acerola fruit — _acerola is a vitamin C source_

**Zinc** (7) · also: Men's Health, Skin, Hair and Nails
- ING-028 Zinc Bisglycinate
- ING-304 Zinc citrate
- ING-305 Zinc picolinate
- ING-311 Zinc oxide
- ING-329 Zinc (unspecified form)
- ING-375 Zinc gluconate
- ING-1061 Zinc Monomethionine / L-OptiZinc

**Mushrooms** (7) · also: Performance and Cognition, Longevity and Anti-aging
- ING-207 mushrooms
- ING-221 Reishi
- ING-225 Cordyceps Mushroom Extract
- ING-234 lion's mane
- ING-306 Turkey tail mushroom extract
- ING-1113 Lignosus rhinocerus / Tiger Milk Mushroom
- ING-1184 Tremella fuciformis

**Immune Support** (24)
- ING-061 Beta glucans
- ING-244 Astragalus Extract
- ING-393 Elderberry, Sambucus
- ING-400 Colostrum
- ING-407 Oregano Oil
- ING-437 Grapefruit Seed Extract
- ING-461 Black Cumin Seed Oil
- ING-474 Thyme Leaf Extract
- ING-479 Lactoferrin
- ING-537 Dextromethorphan `Rx/drug` — _cough medicine (drug)_
- ING-733 Myrrh (resin / oil)
- ING-836 Diphenhydramine `Rx/drug` — _antihistamine (drug); often used for sleep_
- ING-967 Perilla frutescens — _allergy use_
- ING-1111 Immunoglobulins / IgG
- ING-1205 Azelastine `Rx/drug` — _antihistamine (drug)_
- ING-1206 Loratadine `Rx/drug` — _antihistamine (drug)_
- ING-1210 Emtricitabine `Rx/drug` — _HIV PrEP (drug)_
- ING-1211 Tenofovir Disoproxil Fumarate `Rx/drug` — _HIV PrEP (drug)_
- ING-1225 Echinacea (unspecified species)
- ING-1269 Eucalyptus Leaf Extract — _respiratory_
- ING-1272 Cetirizine `Rx/drug` — _antihistamine (drug)_
- ING-1296 Cat's Claw (Uncaria tomentosa) (bark)
- ING-1305 Mullein (leaf) extract — _respiratory_
- ING-1330 Sialic acid

### Skin, Hair and Nails

**Biotin** (1)
- ING-007 Biotin, Vitamin B7

**Collagen** (8) · also: Bone and Joint Health
- ING-149 Collagen Peptides
- ING-378 Hydrolyzed Bovine Hide Collagen Peptides
- ING-381 Fish / Marine collagen peptides
- ING-1110 Horsetail Extract — _hair/skin/nail ingredient_
- ING-1176 Elastin Peptides — _hair/skin/nail ingredient_
- ING-1179 Keratin — _hair/skin/nail ingredient_
- ING-1298 Polypody Vulgare Extract (Polypodium vulgare) (fruit) — _skin / sun protection; Collagen node holds skin-hair-nail ingredients_
- ING-425 Hydrolyzed Chicken Collagen — _Hydrolyzed collagen; existing Collagen secondary goal includes Bone and Joint Health. Un-denatured UC-II remains Joint Support._

### Performance and Cognition

**Protein** (9)
- ING-174 Pea Protein Isolate
- ING-198 whey protein
- ING-530 Protein (unspecified)
- ING-1025 Whole Milk Powder
- ING-1056 Skimmed Milk Powder
- ING-1135 Micellar Casein
- ING-1328 Milk powder
- ING-1057 Soy — _Protein-powder soy defaults to Protein; an isoflavone product should use the specific soy-isoflavones ingredient ING-590._
- ING-330 Brown rice protein — _Same protein family as pea protein._

**Creatine** (1)
- ING-097 Creatine monohydrate

**Amino Acids** (30) · also: Sleep and Recovery
- ING-044 L-leucine
- ING-099 L-Carnosine
- ING-101 Branched chain amino acids
- ING-102 L-isoleucine
- ING-103 L-valine
- ING-116 L-Arginine
- ING-118 L-Lysine
- ING-119 L-Cysteine
- ING-121 L-Threonine
- ING-158 taurine
- ING-239 beta alanine
- ING-240 L-citrulline
- ING-355 L-Phenylalanine
- ING-356 L-Methionine
- ING-357 L-Histidine
- ING-406 L-Ornithine
- ING-465 L-serine
- ING-778 Alanine
- ING-807 Agmatine
- ING-857 Hydroxyproline
- ING-1130 Beta-Hydroxy Beta-Methylbutyrate / HMB
- ING-1131 Citrulline Malate
- ING-1133 L-Arginine Alpha-Ketoglutarate
- ING-1134 L-Norvaline
- ING-1194 D-Phenylalanine
- ING-1242 Aspartic Acid
- ING-1243 Glutamic Acid
- ING-1244 Proline
- ING-1245 Hydroxylysine
- ING-1320 Arginine Nitrate

**Brain Health** (20)
- ING-009 Choline / Vitamin B4 — _choline source; grouped with Alpha-GPC/Citicoline, not B Complex_
- ING-109 Alpha-GPC, alpha-Glycerophosphorylcholine
- ING-110 L-tyrosine — _used for focus_
- ING-125 Ginkgo Biloba Extract
- ING-169 Sunflower Lecithin non-GMO — _phospholipid / choline source_
- ING-226 Huperzine A / Huperzia serrata (toothed clubmoss) extract
- ING-235 cognizin citicoline
- ING-236 Phosphatidylserine
- ING-265 Bacopa Monnieri extract
- ING-279 N-Acetyl L-Tyrosine (NALT)
- ING-358 Uridine
- ING-422 Coffee Fruit Extract — _marketed for BDNF; little caffeine_
- ING-500 Gotu Kola extract
- ING-1049 Nervonic Acid
- ING-1053 Phospholipids
- ING-1054 Phosphatidylcholine
- ING-1192 Triacetyluridine
- ING-1228 Soy Lecithin — _phospholipid source_
- ING-1250 Galantamine
- ING-1254 Sage (Salvia officinalis)

**Nootropics** (11)
- ING-150 Phenylethylamine/ PEA — _phenylethylamine (not palmitoylethanolamide)_
- ING-280 Phenylpiracetam
- ING-1185 Cerebrolysin — _cognitive peptide_
- ING-1190 Noopept
- ING-1191 Semax — _cognitive peptide_
- ING-1193 Vinpocetine
- ING-1204 Selank — _cognitive / anxiolytic peptide_
- ING-1246 Bromantane
- ING-1247 9-Me-BC (9-Methyl-beta-carboline)
- ING-1249 Oroxylum indicum Extract (Sabroxy)
- ING-1278 TAK-653

**Caffeine** (6)
- ING-108 Caffeine
- ING-242 Theobromine — _stimulant_
- ING-415 Nicotine — _stimulant_
- ING-1253 Guarana
- ING-1258 Rutaecarpine — _caffeine-clearance / pre-workout ingredient_
- ING-1293 Eria Jarensis (N,N-dimethylphenethylamine Citrate) — _stimulant_

**ADHD Meds** (6)
- ING-211 Modafinil — _wakefulness agent, grouped with ADHD meds_
- ING-214 Adderall
- ING-215 Ritalin
- ING-959 Atomoxetine
- ING-1189 Lisdexamfetamine
- ING-1248 Adrafinil — _modafinil prodrug_

### Gut and Digestion

**Probiotics** (56) · also: Immune Support
- ING-067 Probiotic / gut microbiota blend
- ING-068 Bifidobacterium longum SD-BB536-JP
- ING-069 Bifidobacterium breve SD-BR3-IT
- ING-070 Lactiplantibacillus plantarum SD-LP1-IT
- ING-071 Lacticaseibacillus rhamnosus SD-LR6-IT
- ING-072 Lacticaseibacillus rhamnosus HRVD113-US
- ING-073 Bifidobacterium infantis SD-M63-JP
- ING-074 Bifidobacterium lactis SD-BS5-IT
- ING-075 Bifidobacterium lactis HRVD524-US
- ING-076 Lactobacillus crispatus SD-LCR01-IT
- ING-077 Lacticaseibacillus casei HRVD300-US
- ING-078 Bifidobacterium breve HRVD521-US
- ING-079 Bifidobacterium longum HRVD90b-US
- ING-080 Bifidobacterium lactis SD-150-BE
- ING-081 Limosilactobacillus fermentum SD-LF8-IT
- ING-082 Lacticaseibacillus rhamnosus SD-GG-BE
- ING-083 Limosilactobacillus reuteri SD-RD830-FR
- ING-084 Bifidobacterium adolescentis SD-BA5-IT
- ING-085 Limosilactobacillus reuteri SD-LRE2-IT
- ING-086 Ligilactobacillus salivarius SD-LS1-IT
- ING-087 Bifidobacterium lactis BPL1 (CECT 8145)
- ING-088 Bifidobacterium longum ES1 (CECT 7347)
- ING-089 Lacticaseibacillus casei CECT 9104
- ING-090 Lactiplantibacillus plantarum SD-LPLDL-UK
- ING-091 Bifidobacterium lactis SD-MB2409-IT
- ING-163 Lactobacillus acidophilus
- ING-192 Akkermansia muciniphila, WB-STR-0001
- ING-222 streptococcus thermophilus
- ING-224 Saccharomyces boulardii
- ING-382 Bacillus coagulans (SNZ-1969 or IDCC1201)
- ING-446 Lactobacillus paracasei
- ING-448 Bifidobacterium bifidum
- ING-452 Bifidobacterium breve
- ING-470 Pediococcus acidilactici
- ING-489 Bacillus indicus, HU36
- ING-490 Bacillus subtilis, HU58
- ING-491 Bacillus coagulans, SC-208
- ING-492 Bacillus licheniformis, SL-307
- ING-493 Bacillus clausii, SC-109
- ING-527 Slimbiotics Postbiotic — _postbiotic_
- ING-1063 Bacillus coagulans (unspecified strain)
- ING-1064 Bacillus coagulans MTCC 5856
- ING-1068 Bifidobacterium animalis subsp. lactis (unspecified strain)
- ING-1070 Bifidobacterium longum (unspecified strain)
- ING-1077 Lactobacillus casei (unspecified strain)
- ING-1079 Lactobacillus fermentum (unspecified strain)
- ING-1080 Lactobacillus gasseri
- ING-1081 Lactobacillus helveticus
- ING-1083 Lactobacillus johnsonii
- ING-1085 Lactobacillus plantarum (unspecified strain)
- ING-1086 Lactobacillus reuteri (unspecified strain)
- ING-1087 Lactobacillus reuteri DSM 17648 / Pylopass
- ING-1088 Lactobacillus rhamnosus (unspecified strain)
- ING-1090 Lactobacillus salivarius (unspecified strain)
- ING-1096 Streptococcus salivarius
- ING-1218 Bacteriophages (unspecified blend)

**Fiber** (18) · also: Metabolic Health
- ING-062 Prebiotic outer capsule / MAP precursors — _prebiotic_
- ING-172 milled Golden Flaxseed
- ING-177 Fibre
- ING-193 Inulin / Chicory inulin
- ING-328 Arabinogalactan (larch)
- ING-373 Prebiotic base (unspecified)
- ING-394 Psyllium Husk
- ING-469 Xylo-oligosaccharides (XOS)
- ING-707 Pectin
- ING-1019 Citrus Pectin
- ING-1074 Glucomannan
- ING-1209 Fructooligosaccharides / FOS
- ING-1259 Methylcellulose
- ING-1292 carob tree (Ceratonia siliqua L.) fruit extract
- ING-1314 Plantago
- ING-1332 Wheat dextrin
- ING-442 Partially Hydrolyzed Guar Gum — _Prebiotic fiber._
- ING-510 Chicory (Cichorium intybus) — _Default to chicory/inulin fiber; review a chicory-coffee product separately._

**Digestive Enzymes** (22)
- ING-129 Papain
- ING-130 Amylase
- ING-131 Bromelain
- ING-132 Lipase
- ING-134 protease
- ING-136 glucoamylase
- ING-137 Cellulase
- ING-138 lactase
- ING-139 Beta-glucanase
- ING-140 phytase
- ING-141 pectinase
- ING-142 Alpha-Galactosidase
- ING-143 Xylanase
- ING-145 Invertase
- ING-320 Hemicellulase
- ING-397 Betaine HCl — _stomach acid support_
- ING-433 Ox Bile Extract — _fat digestion_
- ING-434 Pancreatin
- ING-435 Papaya Fruit Powder — _papaya as digestive aid_
- ING-604 Chymotrypsin
- ING-842 Trypsin
- ING-1327 Maltase

**Gut Health** (26)
- ING-117 L-Glutamine — _mainly gut-lining use_
- ING-133 Ginger root (Zingiber officinale) — _digestion / nausea_
- ING-408 Marshmallow Root
- ING-409 Aloe Vera
- ING-436 Slippery Elm Bark
- ING-457 Terminalia chebula — _triphala herb_
- ING-471 Licorice root extract
- ING-473 Fennel seed extract
- ING-476 Black walnut hull extract — _parasite cleanse_
- ING-514 Yarrow extract
- ING-713 Famotidine `Rx/drug` — _acid reducer (drug)_
- ING-810 Acetylglucosamine
- ING-1072 Deglycyrrhizinated Licorice / DGL
- ING-1076 Hyoscine Butylbromide `Rx/drug` — _antispasmodic (drug)_
- ING-1091 Mastic Gum
- ING-1092 Mebeverine `Rx/drug` — _IBS antispasmodic (drug)_
- ING-1094 Pantoprazole `Rx/drug` — _PPI (drug)_
- ING-1095 Peppermint
- ING-1098 Zinc-L-Carnosine / Polaprezinc — _zinc-carnosine is a gut-lining product, not a zinc supplement_
- ING-1102 Bibhitaki / Terminalia bellirica — _triphala herb_
- ING-1227 Fennel Oil
- ING-1256 Butyrate
- ING-1275 Mesalamine `Rx/drug` — _IBD drug_
- ING-1294 Mucin
- ING-1295 Okra Extract (Abelmoschus esculentus) (fruit)
- ING-1317 Senna — _laxative_

**Liver Support** (9) · also: Metabolic Health
- ING-262 Artichoke leaf extract (Cynara scolymus)
- ING-405 Calcium D-Glucarate — _detox / estrogen clearance, not a calcium supplement_
- ING-508 Burdock root extract
- ING-516 Tauroursodeoxycholic Acid (TUDCA)
- ING-519 Dandelion root/leaf extract
- ING-626 Silymarin
- ING-1105 Bupleurum Extract
- ING-1114 Milk Thistle Extract
- ING-1282 Sarsaparilla, Indian (Hemidesmus indicus) root

### Eye and Vision Health

**Eye Health** (6)
- ING-022 Lutein
- ING-023 Zeaxanthin
- ING-231 bilberry extract
- ING-245 Marigold Extract — _lutein source_
- ING-1266 Mingmu Dihuang Wan — _TCM eye formula_
- ING-1291 Eyebright Extract (Euphrasia officinalis)

### Metabolic Health

**Blood Sugar** (15)
- ING-168 Cinnamon Organic
- ING-204 Apple Cider Vinegar
- ING-254 Berberine / Berberine HCl
- ING-266 Coleus Forskohlii / Forskolin — _weight management_
- ING-277 Exogenous ketones / BHB salts — _keto / metabolic_
- ING-403 Bitter Melon Extract
- ING-430 Cayenne Pepper — _thermogenic / weight_
- ING-526 Conjugated Linoleic Acid (CLA) — _weight management_
- ING-547 Garcinia Cambogia Extract — _weight management_
- ING-1027 Acetic Acid — _ACV active_
- ING-1122 Dihydroberberine
- ING-1123 Green Coffee Bean Extract — _weight management_
- ING-1129 White Kidney Bean Extract — _weight management_
- ING-1257 Garcinol — _weight management_
- ING-1268 Chitosan — _weight management_

**Heart Health** (16) · also: Longevity and Anti-aging
- ING-053 Hesperidin — _vein/circulation flavonoid (with Diosmin)_
- ING-181 Monacolin K, Red Yeast Rice
- ING-205 Nattokinase
- ING-259 Garlic extract / Allicin
- ING-260 Kyolic aged garlic extract
- ING-264 Policosanol
- ING-404 Serrapeptase — _systemic enzyme, grouped with nattokinase_
- ING-545 Hawthorn Leaf With Flower
- ING-748 Diosmin
- ING-1120 Beetroot — _nitrate / blood pressure_
- ING-1121 Citrus Bergamot Extract
- ING-1222 1-Octacosanol / Octacosanol — _policosanol component_
- ING-1234 Hawthorn Berry
- ING-1303 Butcher's Broom
- ING-1304 Horse Chestnut
- ING-1127 Terminalia arjuna Bark Extract — _Arjuna bark; distinct from Terminalia chebula/bellirica in Triphala._

**GLP-1** (4)
- ING-818 Orlistat — _weight-loss drug, grouped with GLP-1_
- ING-1126 Retatrutide
- ING-1128 Tirzepatide
- ING-1271 Semaglutide

**Metabolic Meds** (7)
- ING-184 metformin — _diabetes / longevity use_
- ING-195 Acetylsalicylic Acid, Baby Aspirin — _cardiovascular_
- ING-257 Armour Thyroid / desiccated thyroid — _thyroid hormone_
- ING-321 Ezetimibe — _cholesterol_
- ING-323 Bempedoic acid — _cholesterol_
- ING-644 Pravastatin — _statin_
- ING-858 Telmisartan — _blood pressure_

### Women's Health

**Women's Health** (20)
- ING-048 Inositol / Myo-inositol — _mainly PCOS/hormonal use_
- ING-049 D-chiro-inositol — _mainly PCOS/hormonal use_
- ING-315 Wild yam root powder
- ING-336 Cranberry extract — _urinary health_
- ING-352 DIM / Diindolylmethane — _estrogen metabolism (also used by men)_
- ING-548 Black Cohosh Extract
- ING-590 Isoflavones
- ING-731 Progesterone `Rx/drug` — _HRT (drug)_
- ING-811 Mannose — _urinary health (D-mannose)_
- ING-923 Estradiol `Rx/drug` — _HRT (drug)_
- ING-950 Levonorgestrel `Rx/drug` — _birth control (drug)_
- ING-1103 Blessed Thistle — _lactation_
- ING-1154 Chaste Tree / Vitex agnus-castus
- ING-1156 Dong Quai Extract
- ING-1169 Red Clover / Trifolium pratense
- ING-1170 Rhapontic Rhubarb Root Extract
- ING-1177 Evening Primrose Oil — _evening primrose, mainly PMS/menopause use_
- ING-1285 Peony — _TCM women's herb_
- ING-1287 Chinese angelica root — _dong quai_
- ING-1302 Uva-Ursi Extract (leaf) (Arctostaphylos uva ursi) — _urinary health_

### Men's Health

**Men's Health** (23) · also: Longevity and Anti-aging
- ING-113 Tongkat Ali / Eurycoma longifolia
- ING-114 Fadogia Agrestis
- ING-123 Nettle Extract — _prostate / testosterone use_
- ING-126 Saw Palmetto Extract
- ING-128 Pumpkin Extract — _prostate_
- ING-233 Mucuna pruriens / Velvet bean extract (L-DOPA) — _L-DOPA; libido/dopamine use_
- ING-402 Tribulus Terrestris
- ING-413 Yohimbine
- ING-460 Fenugreek
- ING-521 PrimaVie Shilajit Fulvic Acid Complex — _shilajit, marketed for testosterone/energy_
- ING-855 Dehydroepiandrosterone — _OTC hormone precursor; also used by women_
- ING-1151 7-Keto DHEA — _OTC hormone precursor_
- ING-1153 Butea superba Extract
- ING-1155 Cistanche tubulosa Extract
- ING-1158 Epimedium / Horny Goat Weed
- ING-1162 Muira Puama Extract
- ING-1165 Pregnenolone — _OTC hormone precursor_
- ING-1166 Pumpkin Seed Oil
- ING-1167 Pygeum africanum Extract
- ING-1251 D-Aspartic Acid
- ING-1252 Damiana
- ING-1306 KaempMax black ginger (Kaempferia parviflora) extract (rhizome) [5,7-dimethoxyflavone]
- ING-1307 Beta-sitosterol (from pine) — _prostate_

**Men's Rx** (7) · also: Skin, Hair and Nails
- ING-275 Testosterone (TRT) — _TRT_
- ING-1157 Enclomiphene
- ING-1159 Finasteride — _hair loss_
- ING-1173 Tadalafil — _ED_
- ING-1182 Minoxidil — _hair loss (also used by women)_
- ING-1279 Oxandrolone — _anabolic_
- ING-1280 Boldenone — _anabolic_

### (excluded)

**EXCLUDE** (9)
- ING-039 Ascorbyl palmitate — _antioxidant preservative / excipient_
- ING-124 Gum Arabic — _usually a gummy/tablet binder; map to Fiber if a standalone acacia-fiber product_
- ING-331 Stevia leaf extract — _sweetener_
- ING-432 Black pepper extract / Piperine (BioPerine) — _absorption enhancer_
- ING-646 Glycerol — _excipient_
- ING-984 Gelatin — _capsule material_
- ING-1093 Microcrystalline Cellulose — _excipient_
- ING-1187 Cocoa Butter — _excipient_
- ING-1331 Sulfate — _counter-ion_
