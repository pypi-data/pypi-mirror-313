resource_classifications = {
    "*",
    "childs_based", # Meaning need to look into child fields to determine classifications
    
    "public", #Anyone Can Access ex: synthetic data 
    "authuser_open", # Any Authenticated Can Access ex: prices of gold, bitcoin etc.
    # "authuser_subscription",
    "authuser_confidential", ## Only User Owner Can Access and Specific Admin
    "authuser_limitedacl" , ## Has to be in the ACL
    "authuser_owner"
    "internal_open", ## Any Internal employees only Can Access ex: public reports, emails etc. 
    "internal_sensitive", ## Many Internal employees Can Access IF meet special condition ex: internal financials summary reports , web and app analytics, list of admin users etc.
    "internal_confidential", ## Few Internal employees Can Access. ex: internal user data, key financials, salaries and bonuses etc
    "internal_limitedacl", ## Has to employee usertype and in the ACL
    "internal_owner"
}


resource_domain = {
    "*",
    ############### GYM #########
    "gym_domain",
    "gym_data_domain",
    "gym_ai_domain",
    ############## ORACLE #########
    "oracle_domain",
    "oracle_historic_prices_domain",
    "oracle_ai_domain",
    "oracle_assests_historic_info_domain",
    "oracle_historic_econometrics_domain",
    "oracle_news_historic_domain",
    "oracle_calendar_domain",
    "oracle_modelinfo_domain",
    "oracle_modelmetrics_domain",
    "oracle_modelpredictions_domain",
    ######### ORGANISATIONS #########
    "organisation_domain",
    ################### USER #########
    "user_domain",
    "user_management_domain",
    "user_portfolio_domain",
    "user_groups_and_roles_domain",
    ############### BUSINESS #########
    "business_domain",
    ############### ANALYTICS #########
    "analytics_domain",
    "system_domain"
}

resource_types =  {
    "db", "sql_db", "nosql_db", "dynamodb",
    "big_query", "big_query_project", "big_query_table", "big_query_column", 
    "big_query_row", "big_query_cell",
    "firestore", "firestore_project", "firestore_collection", 
    "firestore_document","firestore_document_with_timeseries" "firestore_document_field",
    "pandas_dataframe", "spark_dataframe",
    "s3_bucket", "storage_bucket",
    "folder", "file", "json_file", "csv_file", "pdf_file", 
    "unstructured_file", "image", "video", "audio", "text",
    "api", "report", "dashboard", "webpage", "website", "web"
}

organisation_relations = {
    "*",
    "retail_customer",
    "corporate_customer",
    "parent",
    "sister",
    "self",
    "partner",
    "supplier",
    "sponsor",
    "investor",
    "regulator",
    "other"
    }

organisation_industries  = {
    "*",
    "data",
    "government",
    "media",
    "academic",
    "commercial",
    "fund",
    "finance",
    "advisory",
    "hedgefund",
    "bank",
    "vc",
    "pe",
    "construction",
    "healthcare",
    "technology",
    "consulting",
    "retail",
    "non_profit",
    "individual",
    "freelancer",
    "other"
}

licences_types={
    "*",
    ######################################### OPEN or FULL Rights
    "public",
    "open",
    "open_no_tandc",
    "full_rights",
    "full_rights_for_sale",
    "commercial_licence_perpetual",
    "customer_private_tac",
    ######################################### SPECIAL CONDITIONS
    "open_with_tandc",
    "on_special_request",
    "commercial_licence_limited_time",
    "customer_owned_for_sale",
     ######################################### Not for Commercial Use
    "full_rights_not_for_sale",
    "internal_only",
    "academic_licence",
    "not_for_commercial_use",
    "customer_private"
    ######################################### Unknown
    "commercial_licence_not_purchased",
    "web_scrapped",
    "unknown"
}


actions ={"GET",
          "POST",
          "DELETE",
          "PUT",
          "create",
          "batch_create",
          "read", 
          "batch_read",
          "edit",
          "batch_edit",
          "add",
          "batch_add",
          "remove",
          "batch_remove",
          "delete",
          "batch_delete", 
          "rename" ,
          "batch_rename",
          "move",
          "batch_move",
          "download",
          "upload",
          "share"
                }

resource_readable_by={
    "*",
    "all",
    "authenticated",
    "restircted",
    "owner",
    "selected_by_owner",
    "admin",
    "selected_by_admin",
    "super_admin",
    "super_admin_selected",
    "system"
}

resource_updatable_by={
     "*",
    "all",
    "authenticated",
    "restircted",
    "owner",
    "selected_by_owner",
    "admin",
    "selected_by_admin",
    "super_admin",
    "super_admin_selected",
    "system"
}