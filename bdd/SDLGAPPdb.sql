BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tbecerros" (
	"idbece"	INTEGER,
	"aretebece"	NUMERIC,
	"nombrebece"	TEXT,
	"pesobece"	NUMERIC,
	"sexobece"	TEXT,
	"razabece"	TEXT,
	"nacimientobece"	NUMERIC,
	"corralbece"	TEXT,
	"estatusbece"	TEXT,
	"aretemadre"	NUMERIC,
	"aretepadre"	NUMERIC,
	"observacionbece"	TEXT,
	"fotobece"	BLOB
);
CREATE TABLE IF NOT EXISTS "tcorral" (
	"idcorral"	INTEGER,
	"identcorral"	NUMERIC,
	"nomcorral"	TEXT,
	"ubicorral"	TEXT,
	"capmax"	NUMERIC,
	"capactual"	NUMERIC,
	"fechamant"	NUMERIC,
	"condicion"	TEXT,
	"observacioncorral"	TEXT,
	PRIMARY KEY("idcorral" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "tganado" (
	"idgdo"	INTEGER,
	"aretegdo"	NUMERIC,
	"nombregdo"	TEXT,
	"sexogdo"	TEXT,
	"razagdo"	TEXT,
	"nacimientogdo"	NUMERIC,
	"corralgdo"	TEXT,
	"alimentogdo"	TEXT,
	"prodgdo"	TEXT,
	"estatusgdo"	TEXT,
	"observaciongdo"	TEXT,
	"fotogdo"	BLOB,
	"idsaludgdo"	INTEGER,
	"idreprodgdo"	INTEGER,
	PRIMARY KEY("idgdo" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "tpropietarios" (
	"idprop"	INTEGER,
	"nombreprop"	TEXT,
	"telprop"	NUMERIC,
	"correoprop"	TEXT,
	"dirprop"	TEXT,
	"rfcprop"	TEXT,
	"psgprop"	TEXT,
	"uppprop"	TEXT,
	PRIMARY KEY("idprop" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "treprod" (
	"idreprod"	INTEGER,
	"cargada"	TEXT,
	"cantpartos"	NUMERIC,
	"fcargadoactual"	NUMERIC,
	"tecnica"	TEXT,
	"areteanimal"	NUMERIC,
	PRIMARY KEY("idreprod" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "tsalud" (
	"idsalud"	INTEGER,
	"areteanimal"	NUMERIC,
	"nomvet"	TEXT,
	"procedimiento"	TEXT,
	"condicionsalud"	TEXT,
	"fecharev"	NUMERIC,
	"archivo"	BLOB,
	"observacionsalud"	TEXT,
	PRIMARY KEY("idsalud" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "usuarios" (
	"id"	INTEGER,
	"nombre"	TEXT,
	"telefono"	TEXT,
	"usuario"	TEXT,
	"pass"	TEXT,
	"rol"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
