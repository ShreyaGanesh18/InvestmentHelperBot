#!/bin/bash

#
# Creates the Athena database
#

#
# Environment variables to be set in the CodeBuild project
#
# $ATHENA_DB    		Name of the Athena database
# $ATHENA_BUCKET		Name of the S3 bucket where the data is stored
# $ATHENA_BUCKET_REGION		Region for the S3 bucket where the data is stored
# $ATHENA_DB_DESCRIPTION	Description for the Athena database
#

echo "Starting build-db.sh"
echo '$ATHENA_DB' "= $ATHENA_DB"
echo '$ATHENA_BUCKET' "= $ATHENA_BUCKET"
echo '$ATHENA_BUCKET_REGION' "= $ATHENA_BUCKET_REGION"
echo '$ATHENA_DB_DESCRIPTION' "= $ATHENA_DB_DESCRIPTION"
echo

# Create INVESTMENT database
echo "Creating Athena database $ATHENA_DB"
aws glue create-database --database-input "Name=$ATHENA_DB,Description=$ATHENA_DB_DESCRIPTION" >/dev/null

# Create INVESTMENT allfin table in Athena
echo "Creating allfin table..."
aws athena start-query-execution \
    --query-string "create external table allfin ( exchange_date DATE,  "Aarti India" INT, "Aban Offshore" INT, "ABB India" INT, "Abbott India" INT, "ACC" INT, "Adani Enterpris" INT, "Adani Ports" INT, "Adani Power" INT, "Adani Trans" INT, "Aditya Birla F" INT, "Advanced Enzyme" INT, "Aegis Logistics" INT, "AIA Engineering" INT, "Ajanta Pharma" INT, "Akzo Nobel" INT, "Alembic Pharma" INT, "Alkem Lab" INT, "Allahabad Bank" INT, "Allcargo" INT, "Amara Raja Batt" INT, "Ambuja Cements" INT, "Andhra Bank" INT, "Apar Ind" INT, "APL Apollo" INT, "Apollo Hospital" INT, "Apollo Tyres" INT, "Arvind" INT, "Asahi India" INT, "Ashok Leyland" INT, "Ashoka Buildcon" INT, "Asian Paints" INT, "Astra Microwave" INT, "Astral Poly Tec" INT, "AstraZeneca" INT, "Atul" INT, "Aurobindo Pharm" INT, "Avanti Feeds" INT, "Avenue Supermar" INT, "Axis Bank" INT, "Bajaj Auto" INT, "Bajaj Consumer" INT, "Bajaj Electric" INT, "Bajaj Finance" INT, "Bajaj Finserv" INT, "Bajaj Hindustha" INT, "Bajaj Holdings" INT, "Balkrishna Ind" INT, "Balmer Lawrie" INT, "Balrampur Chini" INT, "Bank of Baroda" INT, "Bank of India" INT, "Bank of Mah" INT, "BASF" INT, "Bata India" INT, "Bayer CropScien" INT, "BEML" INT, "Berger Paints" INT, "BF Utilities" INT, "Bharat Elec" INT, "Bharat Fin" INT, "Bharat Forge" INT, "Bharti Airtel" INT, "Bharti Infratel" INT, "BHEL" INT, "Biocon" INT, "Birla Corp" INT, "Birlasoft" INT, "Bliss GVS" INT, "Blue Dart" INT, "Blue Star" INT, "Bombay Burmah" INT, "Bombay Dyeing" INT, "Bosch" INT, "BPCL" INT, "Britannia" INT, "Cadila Health" INT, "Can Fin Homes" INT, "Canara Bank" INT, "Capital First" INT, "Caplin Labs" INT, "Carborundum" INT, "CARE" INT, "Castrol" INT, "CCL Products" INT, "Ceat" INT, "Central Bank" INT, "Century" INT, "CenturyPlyboard" INT, "Cera Sanitary" INT, "CESC" INT, "CG Consumer" INT, "CG Power" INT, "Chambal Fert" INT, "Chennai Petro" INT, "Cholamandalam" INT, "Cipla" INT, "City Union Bank" INT, "Coal India" INT, "Coffee Day" INT, "Colgate" INT, "Container Corp" INT, "Coromandel Int" INT, "Corporation Bk" INT, "Cox Kings" INT, "CRISIL" INT, "Cummins" INT, "Cyient" INT, "Dabur India" INT, "Dalmia Bharat" INT, "DB Corp" INT, "DCB Bank" INT, "DCM Shriram" INT, "Deepak Fert" INT, "Delta Corp" INT, "Den Networks" INT, "Dena Bank" INT, "Dewan Housing" INT, "Dhanuka Agritec" INT, "Dilip Buildcon" INT, "Dish TV" INT, "Divis Labs" INT, "DLF" INT, "Dr Lal PathLab" INT, "Dr Reddys Labs" INT, "eClerx Services" INT, "Edelweiss" INT, "Eicher Motors" INT, "EID Parry" INT, "EIH" INT, "Elgi Equipments" INT, "Emami" INT, "Endurance Techn" INT, "EngineersInd" INT, "Ent Network Ind" INT, "Equitas Holding" INT, "Eros Intl" INT, "Escorts" INT, "Essel Propack" INT, "Eveready Ind" INT, "Exide Ind" INT, "FDC" INT, "Federal Bank" INT, "Finolex Cables" INT, "Finolex Ind" INT, "Firstsource Sol" INT, "Force Motors" INT, "Fortis Health" INT, "Future Consumer" INT, "Future Life" INT, "Future Retail" INT, "GAIL" INT, "Gateway Distri" INT, "Gati" INT, "Gayatri Project" INT, "GE Power India" INT, "GE Shipping" INT, "GE ThD India" INT, "GIC Housing Fin" INT, "Gillette India" INT, "GlaxoSmith Con" INT, "GlaxoSmithKline" INT, "Glenmark" INT, "GMR Infra" INT, "GNFC" INT, "Godfrey Phillip" INT, "Godrej Consumer" INT, "Godrej Ind" INT, "Godrej Prop" INT, "Granules India" INT, "Grasim" INT, "Greaves Cotton" INT, "Greenply Ind" INT, "Grindwell Norto" INT, "GRUH Finance" INT, "GSFC" INT, "Guj Alkali" INT, "Guj Flourochem" INT, "Guj Heavy Chem" INT, "Guj Mineral" INT, "Guj State Petro" INT, "Gujarat Gas" INT, "Gujarat Pipavav" INT, "Gulf Oil Lubric" INT, "Hathway Cable" INT, "Hatsun Agro" INT, "Havells India" INT, "HCL Info" INT, "HCL Tech" INT, "HDFC" INT, "HDFC Bank" INT, "HDIL" INT, "Heidelberg Cem" INT, "Heritage Foods" INT, "Hero Motocorp" INT, "Hexaware Tech" INT, "HFCL" INT, "Himatsingka Sei" INT, "Hind Constr" INT, "Hind Copper" INT, "Hind Zinc" INT, "Hindalco" INT, "Honeywell Autom" INT, "HPCL" INT, "HSIL" INT, "HUL" INT, "ICICI Bank" INT, "ICICI Prudentia" INT, "ICRA" INT, "IDBI Bank" INT, "IDFC" INT, "IDFC First Bank" INT, "IFCI" INT, "IGL" INT, "IIFL Holdings" INT, "ILandFS Trans" INT, "India Cements" INT, "Indiabulls Hsg" INT, "Indiabulls Real" INT, "Indiabulls Vent" INT, "Indian Bank" INT, "Indian Hotels" INT, "Indo Count" INT, "Indoco Remedies" INT, "IndusInd Bank" INT, "Infibeam Avenue" INT, "Info Edge" INT, "Infosys" INT, "Ingersoll Rand" INT, "INOX Leisure" INT, "Inox Wind" INT, "Intellect Desig" INT, "Interglobe Avi" INT, "IOB" INT, "IOC" INT, "Ipca Labs" INT, "IRB Infra" INT, "ISGEC Heavy Eng" INT, "ITC" INT, "ITD Cementation" INT, "J Kumar Infra" INT, "J. K. Cement" INT, "JagranPrakashan" INT, "Jai Corp" INT, "Jain Irrigation" INT, "Jaiprakash Asso" INT, "JB Chemicals" INT, "JBF Industries" INT, "Jet Airways" INT, "Jindal Hisar" INT, "Jindal PolyFilm" INT, "Jindal Saw" INT, "Jindal Steel" INT, "JK Bank" INT, "JK Lakshmi Cem" INT, "JK Tyre  Ind" INT, "JM Financial" INT, "Johnson Control" INT, "JSW Energy" INT, "JSW Steel" INT, "Jubilant Food" INT, "Jubilant Life" INT, "Just Dial" INT, "Jyothy Labs" INT, "Kajaria Ceramic" INT, "Kalpataru Power" INT, "Kansai Nerolac" INT, "Karnataka Bank" INT, "Kaveri Seed" INT, "KEC Intl" INT, "Kesoram" INT, "Kirloskar Oil" INT, "Kitex Garments" INT, "Kotak Mahindra" INT, "KPR Mill" INT, "KRBL" INT, "Kwality" INT, "LT Finance" INT, "LT Infotech" INT, "LT Technology" INT, "La Opala RG" INT, "Lakshmi Machine" INT, "Lakshmi Vilas" INT, "Larsen" INT, "Laurus Labs" INT, "LIC Housing Fin" INT, "Linde India" INT, "Lupin" INT, "MM" INT, "MM Financial" INT, "Magma Fincorp" INT, "Mahanagar Gas" INT, "Mahindra CIE" INT, "Mahindra Holida" INT, "Mahindra Life" INT, "Manappuram Fin" INT, "Manpasand Bever" INT, "Marico" INT, "Marksans Pharma" INT, "Maruti Suzuki" INT, "Max Financial" INT, "Max India" INT, "Mcleod" INT, "MCX India" INT, "Minda Ind" INT, "Mindtree" INT, "MMTC Ltd" INT, "MOIL" INT, "Monsanto India" INT, "Motherson Sumi" INT, "Motilal Oswal" INT, "MphasiS" INT, "MRF" INT, "MRPL" INT, "MTNL" INT, "Muthoot Finance" INT, "NALCO" INT, "Narayana Hruda" INT, "Natco Pharma" INT, "Nava Bharat Ven" INT, "Navin Fluorine" INT, "Navkar Corp" INT, "Navneet" INT, "NBCC India" INT, "NCC" INT, "Nestle" INT, "Network18" INT, "NHPC" INT, "NIIT" INT, "NIIT Tech" INT, "Nilkamal" INT, "NLC India" INT, "NMDC" INT, "NTPC" INT ) ROW FORMAT DELIMITED FIELDS TERMINATED BY "|" LOCATION "$ATHENA_BUCKET/allfin";" \
    --query-execution-context "Database=$ATHENA_DB" \
    --result-configuration "OutputLocation=$ATHENA_BUCKET/output/" \
    >/dev/null

# Create INVESTMENT my_portfolio table in Athena
echo "Creating my_portfolio table..."
aws athena start-query-execution \
    --query-string "create external table my_portfolio (security_type STRING, company_name STRING, current_stock_price DECIMAL(10,4), percentage_change DECIMAL(10,4), quantity INT, investment INT, average_price DECIMAL(15,4), day_gain INT, day_gain_fraction DECIMAL(15,4),overall_gain INT, overall_gain_fraction DECIMAL(15,4),latest_value INT)   ROW FORMAT DELIMITED FIELDS TERMINATED BY '|' LOCATION '$ATHENA_BUCKET/my_portfolio';" \
    --query-execution-context "Database=$ATHENA_DB" \
    --result-configuration "OutputLocation=$ATHENA_BUCKET/output/" \
    >/dev/null
# Create INVESTMENT company table in Athena
echo "Creating COMPANY table..."
aws athena start-query-execution \
    --query-string "create external table company (company_name STRING)   ROW FORMAT DELIMITED FIELDS TERMINATED BY '|' LOCATION '$ATHENA_BUCKET/company';" \
    --query-execution-context "Database=$ATHENA_DB" \
    --result-configuration "OutputLocation=$ATHENA_BUCKET/output/" \
    >/dev/null

# Create INVESTMENT date table in Athena
echo "Creating transaction_history table..."
aws athena start-query-execution \
    --query-string "create external table transaction_history (transaction_date DATE, company_name STRING, transaction_type STRING, quantity INT, price INT, value INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY '|' LOCATION '$ATHENA_BUCKET/transaction_history';" \
    --query-execution-context "Database=$ATHENA_DB" \
    --result-configuration "OutputLocation=$ATHENA_BUCKET/output/" \
    >/dev/null
