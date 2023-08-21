-- deploy_host_record definition
CREATE TABLE "deploy_host_record" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "vm_id" varchar(64) NOT NULL,
  "ip" varchar(15) NOT NULL,
  "port" varchar(6) NOT NULL,
  "vm_name" varchar(100) NOT NULL,
  "create_time" datetime NOT NULL,
  "pm_ip" varchar(15) NOT NULL,
  "pm_port" varchar(5) NOT NULL
);


-- host_status_record definition
CREATE TABLE "host_status_record" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "vm_id" varchar(64) NOT NULL,
  "ip" varchar(15) NOT NULL,
  "port" varchar(6) NOT NULL,
  "vm_name" varchar(100) NOT NULL,
  "status" varchar(10) NOT NULL,
  "create_time" datetime NOT NULL,
  "pm_ip" varchar(15) NOT NULL,
  "pm_port" varchar(5) NOT NULL,
  "update_time" datetime NOT NULL
);


-- host_register_info definition
CREATE TABLE "host_register_info" (
  "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  "host_type" varchar(2) NOT NULL,
  "vm_ip" varchar(15) NOT NULL,
  "pm_ip" varchar(15) NOT NULL,
  "create_time" datetime NOT NULL,
  "update_time" datetime NOT NULL
);
