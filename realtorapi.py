import json
import requests
import pandas as pd
from tabulate import tabulate
from pprint import pprint


class RealtorScraper:
    def __init__(self, page_numbers: int) -> None:
        self.page_numbers = page_numbers

    def send_request(self, page_number: int, offset_parameter: int) -> dict:

        url = "https://www.realtor.com/api/v1/rdc_search_srp?client_id=rdc-search-rentals&schema=vesta"
        headers = {"content-type": "application/json"}

        body = r'{"query":"\n\nquery ConsumerSearchMainQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $sort_type: SearchSortType, $client_data: JSON, $geoSupportedSlug: String!, $bucket: SearchAPIBucket, $by_prop_type: [String])\n{\n  home_search: home_search(query: $query,\n    sort: $sort,\n    limit: $limit,\n    offset: $offset,\n    sort_type: $sort_type,\n    client_data: $client_data,\n    bucket: $bucket,\n  ){\n    count\n    total\n    results {\n      property_id\n      list_price\n      primary_photo (https: true){\n        href\n      }\n      source {\n        id\n        agents{\n          office_name\n        }\n        type\n        spec_id\n        plan_id\n      }\n      community {\n        property_id\n        description {\n          name\n        }\n        advertisers{\n          office{\n            hours\n            phones {\n              type\n              number\n            }\n          }\n          builder {\n            fulfillment_id\n          }\n        }\n      }\n      products {\n        brand_name\n        products\n      }\n      listing_id\n      matterport\n      virtual_tours{\n        href\n        type\n      }\n      status\n      permalink\n      price_reduced_amount\n      other_listings{rdc {\n      listing_id\n      status\n      listing_key\n      primary\n    }}\n      description{\n        beds\n        baths\n        baths_full\n        baths_half\n        baths_1qtr\n        baths_3qtr\n        garage\n        stories\n        type\n        sub_type\n        lot_sqft\n        sqft\n        year_built\n        sold_price\n        sold_date\n        name\n      }\n      location{\n        street_view_url\n        address{\n          line\n          postal_code\n          state\n          state_code\n          city\n          coordinate {\n            lat\n            lon\n          }\n        }\n        county {\n          name\n          fips_code\n        }\n      }\n      tax_record {\n        public_record_id\n      }\n      lead_attributes {\n        show_contact_an_agent\n        opcity_lead_attributes {\n          cashback_enabled\n          flip_the_market_enabled\n        }\n        lead_type\n      }\n      open_houses {\n        start_date\n        end_date\n        description\n        methods\n        time_zone\n        dst\n      }\n      flags{\n        is_coming_soon\n        is_pending\n        is_foreclosure\n        is_contingent\n        is_new_construction\n        is_new_listing (days: 14)\n        is_price_reduced (days: 30)\n        is_plan\n        is_subdivision\n      }\n      list_date\n      last_update_date\n      coming_soon_date\n      photos(limit: 2, https: true){\n        href\n      }\n      tags\n      branding {\n        type\n        photo\n        name\n      }\n    }\n  }\n  geo(slug_id: $geoSupportedSlug) {\n    parents {\n      geo_type\n      slug_id\n      name\n    }\n    geo_statistics(group_by: property_type) {\n      housing_market {\n        by_prop_type(type: $by_prop_type){\n          type\n           attributes{\n            median_listing_price\n            median_lot_size\n            median_sold_price\n            median_price_per_sqft\n            median_days_on_market\n          }\n        }\n        listing_count\n        median_listing_price\n        median_rent_price\n        median_price_per_sqft\n        median_days_on_market\n        median_sold_price\n        month_to_month {\n          active_listing_count_percent_change\n          median_days_on_market_percent_change\n          median_listing_price_percent_change\n          median_listing_price_sqft_percent_change\n        }\n      }\n    }\n    recommended_cities: recommended(query: {geo_search_type: city, limit: 20}) {\n      geos {\n        ... on City {\n          city\n          state_code\n          geo_type\n          slug_id\n        }\n        geo_statistics(group_by: property_type) {\n          housing_market {\n            by_prop_type(type: [\"home\"]) {\n              type\n              attributes {\n                median_listing_price\n              }\n            }\n            median_listing_price\n          }\n        }\n      }\n    }\n    recommended_neighborhoods: recommended(query: {geo_search_type: neighborhood, limit: 20}) {\n      geos {\n        ... on Neighborhood {\n          neighborhood\n          city\n          state_code\n          geo_type\n          slug_id\n        }\n        geo_statistics(group_by: property_type) {\n          housing_market {\n            by_prop_type(type: [\"home\"]) {\n              type\n              attributes {\n                median_listing_price\n              }\n            }\n            median_listing_price\n          }\n        }\n      }\n    }\n    recommended_counties: recommended(query: {geo_search_type: county, limit: 20}) {\n      geos {\n        ... on HomeCounty {\n          county\n          state_code\n          geo_type\n          slug_id\n        }\n        geo_statistics(group_by: property_type) {\n          housing_market {\n            by_prop_type(type: [\"home\"]) {\n              type\n              attributes {\n                median_listing_price\n              }\n            }\n            median_listing_price\n          }\n        }\n      }\n    }\n    recommended_zips: recommended(query: {geo_search_type: postal_code, limit: 20}) {\n      geos {\n        ... on PostalCode {\n          postal_code\n          geo_type\n          slug_id\n        }\n        geo_statistics(group_by: property_type) {\n          housing_market {\n            by_prop_type(type: [\"home\"]) {\n              type\n              attributes {\n                median_listing_price\n              }\n            }\n            median_listing_price\n          }\n        }\n      }\n    }\n  }\n}","variables":{"query":{"status":["for_sale","ready_to_build"],"primary":true,"state_code":"NY"},"client_data":{"device_data":{"device_type":"web"},"user_data":{"last_view_timestamp":-1}},"limit":42,"offset":42,"zohoQuery":{"silo":"search_result_page","location":"New York","property_status":"for_sale","filters":{},"page_index":"2"},"sort_type":"relevant","geoSupportedSlug":"","by_prop_type":["home"]},"operationName":"ConsumerSearchMainQuery","callfrom":"SRP","nrQueryType":"MAIN_SRP","visitor_id":"eff16470-ceb5-4926-8c0b-6d1779772842","isClient":true,"seoPayload":{"asPath":"/realestateandhomes-search/New-York/pg-2","pageType":{"silo":"search_result_page","status":"for_sale"},"county_needed_for_uniq":false}}'
        # body =r'{"query":"\nquery ConsumerSearchQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $bucket: SearchAPIBucket) {\n  home_search(query: $query, sort: $sort, limit: $limit, offset: $offset, bucket: $bucket) {\n    costar_counts {\n      costar_total\n      non_costar_total\n    }\n    total\n    count\n    properties: results {\n      property_id\n      listing_id\n      list_price\n      list_price_max\n      list_price_min\n      permalink\n      price_reduced_amount\n      matterport\n      virtual_tours {\n        href\n      }\n      status\n      list_date\n      lead_attributes {\n        lead_type\n      }\n      pet_policy {\n        cats\n        dogs\n        dogs_small\n        dogs_large\n      }\n      other_listings {\n        rdc{\n          listing_id,\n          status\n        }\n      }\n      flags {\n        is_pending\n      }\n      photos(limit: 2, https: true) {\n        href\n      }\n      primary_photo(https: true) {\n          href\n      }\n      advertisers {\n        office {\n          name\n          phones {\n            number\n            type\n            primary\n            trackable\n            ext\n          }\n        }\n        phones {\n          number\n          type\n          primary\n          trackable\n          ext\n        }\n      }\n      flags {\n        is_new_listing\n      }\n      location {\n        address {\n          line\n          city\n          coordinate {\n            lat\n            lon\n          }\n          country\n          state_code\n          postal_code\n        }\n        county {\n          name\n          fips_code\n        }\n      }\n      description {\n        beds\n        beds_max\n        beds_min\n        baths\n        baths_min\n        baths_max\n        baths_full\n        baths_full_calc\n        baths_half\n        baths_3qtr\n        baths_1qtr\n        garage\n        garage_min\n        garage_max\n        sqft\n        sqft_max\n        sqft_min\n        lot_sqft\n        name\n        sub_type\n        type\n        year_built\n      }\n      units {\n        availability {\n          date\n        }\n        description {\n          baths\n          beds\n          sqft\n        }\n        list_price\n      }\n      branding {\n        type\n        photo\n        name\n      }\n      source {\n        id\n        type\n      }\n    }\n  }\n}\n","variables":{"geoSupportedSlug":"","query":{"primary":true,"status":["for_rent"],"state_code":"CO","pending":false},"limit":42,"offset":42,"bucket":{"sort":"rentalModelV2_1","sort_options":{"costar_total":1311,"non_costar_total":5992,"variation":"costar_basic"}}},"seoPayload":{"asPath":"/apartments/Colorado/","pageType":{"silo":"search_result_page","status":"for_rent"},"county_needed_for_uniq":false}}'
        # body = r'{"query":"\nquery ConsumerSearchQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $bucket: SearchAPIBucket) {\n  home_search: home_search(query: $query, sort: $sort, limit: $limit, offset: $offset, bucket: $bucket) {\n    costar_counts {\n      costar_total\n      non_costar_total\n    }\n    count\n    total\n    aggregation\n    properties: results {\n      permalink\n      lead_attributes {\n        show_contact_an_agent\n      }\n      branding {\n        type\n        photo\n        name\n      }\n      price_reduced_date\n      price_reduced_amount\n      matterport\n      virtual_tours {\n        href\n      }\n      advertisers {\n        email\n        fulfillment_id\n        href\n        mls_set\n        name\n        nrds_id\n        office {\n          email\n          fulfillment_id\n          mls_set\n          href\n          name\n          phones {\n            ext\n            number\n            primary\n            trackable\n            type\n          }\n        }\n        phones {\n          ext\n          number\n          primary\n          trackable\n          type\n        }\n      }\n      description {\n        baths\n        baths_full\n        baths_full_calc\n        baths_half\n        baths_3qtr\n        baths_1qtr\n        beds\n        garage\n        lot_sqft\n        name\n        sqft\n        sub_type\n        type\n        year_built\n        baths_min\n        baths_max\n        beds_max\n        beds_min\n        garage_min\n        garage_max\n        sqft_max\n        sqft_min\n      }\n      flags {\n        is_pending\n        is_deal_available\n        is_for_rent\n        is_garage_present\n        is_senior_community\n        is_new_listing(days: 3)\n      }\n      href\n      last_price_change_amount\n      last_price_change_date\n      last_update_date\n      list_date\n      list_price\n      list_price_min\n      list_price_max\n      listing_id\n      location {\n        address {\n          city\n          coordinate {\n            lat\n            lon\n          }\n          country\n          line\n          postal_code\n          state\n          state_code\n          street_direction\n          street_name\n          street_number\n          street_post_direction\n          street_suffix\n          unit\n        }\n        county {\n          fips_code\n          name\n          state_code\n        }\n        search_areas {\n          city\n          state_code\n        }\n      }\n      photo_count\n      photos(limit: 3, https: true) {\n        description\n        href\n        type\n        title\n        tags {\n          label\n          probability\n        }\n      }\n      pet_policy {\n        cats\n        dogs\n        text\n      }\n      primary_photo(https: true) {\n        description\n        href\n        type\n      }\n      open_houses {\n        description\n        end_date\n        start_date\n        time_zone\n        dst\n      }\n      other_listings {\n        rdc {\n          listing_id\n          status\n          primary\n        }\n      }\n      products {\n        product_attributes\n        products\n      }\n      property_history {\n        listing {\n          photos {\n            href\n          }\n        }\n      }\n      property_id\n      source {\n        agents {\n          agent_id\n          agent_name\n        }\n        id\n        listing_id\n        community_id\n        name\n        type\n      }\n      status\n      suppression_flags\n      tags\n      when_indexed\n      source {\n        tier_rank\n        id\n      }\n      community_metrics {\n        leads_month_to_date\n        active_listing_count\n        community_price_per_lead\n      }\n    }\n    property_types: seo_linking_modules(type: top_property_types) {\n      title\n      linking_module {\n        title\n        url\n      }\n    }\n  }\n  meta\n}\n","variables":{"geoSupportedSlug":"","query":{"primary":true,"status":["for_rent"],"state_code":"TX","pending":false,"community_price_per_lead":{"min":0}},"limit":42,"offset":42,"bucket":{"sort":"rentalModelV2_1","sort_options":{"costar_total":0,"non_costar_total":0,"variation":"costar_basic"}},"sort":{"field":"community_price_per_lead","direction":"desc"}},"seoPayload":{"asPath":"/apartments/Texas","pageType":{"silo":"search_result_page","status":"for_rent"},"county_needed_for_uniq":false}}'
        # body = r'{"query":"\nquery ConsumerSearchQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $bucket: SearchAPIBucket) {\n  home_search: home_search(query: $query, sort: $sort, limit: $limit, offset: $offset, bucket: $bucket) {\n    costar_counts {\n      costar_total\n      non_costar_total\n    }\n    count\n    total\n    aggregation\n    properties: results {\n      permalink\n      lead_attributes {\n        show_contact_an_agent\n      }\n      branding {\n        type\n        photo\n        name\n      }\n      price_reduced_date\n      price_reduced_amount\n      matterport\n      virtual_tours {\n        href\n      }\n      advertisers {\n        email\n        fulfillment_id\n        href\n        mls_set\n        name\n        nrds_id\n        office {\n          email\n          fulfillment_id\n          mls_set\n          href\n          name\n          phones {\n            ext\n            number\n            primary\n            trackable\n            type\n          }\n        }\n        phones {\n          ext\n          number\n          primary\n          trackable\n          type\n        }\n      }\n      description {\n        baths\n        baths_full\n        baths_full_calc\n        baths_half\n        baths_3qtr\n        baths_1qtr\n        beds\n        garage\n        lot_sqft\n        name\n        sqft\n        sub_type\n        type\n        year_built\n        baths_min\n        baths_max\n        beds_max\n        beds_min\n        garage_min\n        garage_max\n        sqft_max\n        sqft_min\n      }\n      flags {\n        is_pending\n        is_deal_available\n        is_for_rent\n        is_garage_present\n        is_senior_community\n        is_new_listing(days: 3)\n      }\n      href\n      last_price_change_amount\n      last_price_change_date\n      last_update_date\n      list_date\n      list_price\n      list_price_min\n      list_price_max\n      listing_id\n      location {\n        address {\n          city\n          coordinate {\n            lat\n            lon\n          }\n          country\n          line\n          postal_code\n          state\n          state_code\n          street_direction\n          street_name\n          street_number\n          street_post_direction\n          street_suffix\n          unit\n        }\n        county {\n          fips_code\n          name\n          state_code\n        }\n        search_areas {\n          city\n          state_code\n        }\n      }\n      photo_count\n      photos(limit: 3, https: true) {\n        description\n        href\n        type\n        title\n        tags {\n          label\n          probability\n        }\n      }\n      pet_policy {\n        cats\n        dogs\n        text\n      }\n      primary_photo(https: true) {\n        description\n        href\n        type\n      }\n      open_houses {\n        description\n        end_date\n        start_date\n        time_zone\n        dst\n      }\n      other_listings {\n        rdc {\n          listing_id\n          status\n          primary\n        }\n      }\n      products {\n        product_attributes\n        products\n      }\n      property_history {\n        listing {\n          photos {\n            href\n          }\n        }\n      }\n      property_id\n      source {\n        agents {\n          agent_id\n          agent_name\n        }\n        id\n        listing_id\n        community_id\n        name\n        type\n      }\n      status\n      suppression_flags\n      tags\n      when_indexed\n      source {\n        tier_rank\n        id\n      }\n      community_metrics {\n        leads_month_to_date\n        active_listing_count\n        community_price_per_lead\n      }\n    }\n    property_types: seo_linking_modules(type: top_property_types) {\n      title\n      linking_module {\n        title\n        url\n      }\n    }\n  }\n  meta\n}\n","variables":{"geoSupportedSlug":"","query":{"primary":true,"status":["for_rent"],"state_code":"NY","pending":false,"community_price_per_lead":{"min":0}},"limit":42,"offset":42,"bucket":{"sort":"rentalModelV2_1","sort_options":{"costar_total":0,"non_costar_total":0,"variation":"costar_basic"}},"sort":{"field":"community_price_per_lead","direction":"desc"}},"seoPayload":{"asPath":"/apartments/New-York","pageType":{"silo":"search_result_page","status":"for_rent"},"county_needed_for_uniq":false}}'
        # body = r'{"query":"\nquery ConsumerSearchQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $bucket: SearchAPIBucket) {\n  home_search: home_search(query: $query, sort: $sort, limit: $limit, offset: $offset, bucket: $bucket) {\n    costar_counts {\n      costar_total\n      non_costar_total\n    }\n    count\n    total\n    aggregation\n    properties: results {\n      permalink\n      lead_attributes {\n        show_contact_an_agent\n      }\n      branding {\n        type\n        photo\n        name\n      }\n      price_reduced_date\n      price_reduced_amount\n      matterport\n      virtual_tours {\n        href\n      }\n      advertisers {\n        email\n        fulfillment_id\n        href\n        mls_set\n        name\n        nrds_id\n        office {\n          email\n          fulfillment_id\n          mls_set\n          href\n          name\n          phones {\n            ext\n            number\n            primary\n            trackable\n            type\n          }\n        }\n        phones {\n          ext\n          number\n          primary\n          trackable\n          type\n        }\n      }\n      description {\n        baths\n        baths_full\n        baths_full_calc\n        baths_half\n        baths_3qtr\n        baths_1qtr\n        beds\n        garage\n        lot_sqft\n        name\n        sqft\n        sub_type\n        type\n        year_built\n        baths_min\n        baths_max\n        beds_max\n        beds_min\n        garage_min\n        garage_max\n        sqft_max\n        sqft_min\n      }\n      flags {\n        is_pending\n        is_deal_available\n        is_for_rent\n        is_garage_present\n        is_senior_community\n        is_new_listing(days: 3)\n      }\n      href\n      last_price_change_amount\n      last_price_change_date\n      last_update_date\n      list_date\n      list_price\n      list_price_min\n      list_price_max\n      listing_id\n      location {\n        address {\n          city\n          coordinate {\n            lat\n            lon\n          }\n          country\n          line\n          postal_code\n          state\n          state_code\n          street_direction\n          street_name\n          street_number\n          street_post_direction\n          street_suffix\n          unit\n        }\n        county {\n          fips_code\n          name\n          state_code\n        }\n        search_areas {\n          city\n          state_code\n        }\n      }\n      photo_count\n      photos(limit: 3, https: true) {\n        description\n        href\n        type\n        title\n        tags {\n          label\n          probability\n        }\n      }\n      pet_policy {\n        cats\n        dogs\n        text\n      }\n      primary_photo(https: true) {\n        description\n        href\n        type\n      }\n      open_houses {\n        description\n        end_date\n        start_date\n        time_zone\n        dst\n      }\n      other_listings {\n        rdc {\n          listing_id\n          status\n          primary\n        }\n      }\n      products {\n        product_attributes\n        products\n      }\n      property_history {\n        listing {\n          photos {\n            href\n          }\n        }\n      }\n      property_id\n      source {\n        agents {\n          agent_id\n          agent_name\n        }\n        id\n        listing_id\n        community_id\n        name\n        type\n      }\n      status\n      suppression_flags\n      tags\n      when_indexed\n      source {\n        tier_rank\n        id\n      }\n      community_metrics {\n        leads_month_to_date\n        active_listing_count\n        community_price_per_lead\n      }\n    }\n    property_types: seo_linking_modules(type: top_property_types) {\n      title\n      linking_module {\n        title\n        url\n      }\n    }\n  }\n  meta\n}\n","variables":{"geoSupportedSlug":"","query":{"primary":true,"status":["for_rent"],"state_code":"CO","pending":false,"community_price_per_lead":{"min":0}},"limit":42,"offset":42,"bucket":{"sort":"rentalModelV2_1","sort_options":{"costar_total":0,"non_costar_total":0,"variation":"costar_basic"}},"sort":{"field":"community_price_per_lead","direction":"desc"}},"seoPayload":{"asPath":"/apartments/Colorado","pageType":{"silo":"search_result_page","status":"for_rent"},"county_needed_for_uniq":false}}'
        # body = r'{"query":"\nquery ConsumerSearchQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $bucket: SearchAPIBucket) {\n  home_search: home_search(query: $query, sort: $sort, limit: $limit, offset: $offset, bucket: $bucket) {\n    costar_counts {\n      costar_total\n      non_costar_total\n    }\n    count\n    total\n    aggregation\n    properties: results {\n      permalink\n      lead_attributes {\n        show_contact_an_agent\n      }\n      branding {\n        type\n        photo\n        name\n      }\n      price_reduced_date\n      price_reduced_amount\n      matterport\n      virtual_tours {\n        href\n      }\n      advertisers {\n        email\n        fulfillment_id\n        href\n        mls_set\n        name\n        nrds_id\n        office {\n          email\n          fulfillment_id\n          mls_set\n          href\n          name\n          phones {\n            ext\n            number\n            primary\n            trackable\n            type\n          }\n        }\n        phones {\n          ext\n          number\n          primary\n          trackable\n          type\n        }\n      }\n      description {\n        baths\n        baths_full\n        baths_full_calc\n        baths_half\n        baths_3qtr\n        baths_1qtr\n        beds\n        garage\n        lot_sqft\n        name\n        sqft\n        sub_type\n        type\n        year_built\n        baths_min\n        baths_max\n        beds_max\n        beds_min\n        garage_min\n        garage_max\n        sqft_max\n        sqft_min\n      }\n      flags {\n        is_pending\n        is_deal_available\n        is_for_rent\n        is_garage_present\n        is_senior_community\n        is_new_listing(days: 3)\n      }\n      href\n      last_price_change_amount\n      last_price_change_date\n      last_update_date\n      list_date\n      list_price\n      list_price_min\n      list_price_max\n      listing_id\n      location {\n        address {\n          city\n          coordinate {\n            lat\n            lon\n          }\n          country\n          line\n          postal_code\n          state\n          state_code\n          street_direction\n          street_name\n          street_number\n          street_post_direction\n          street_suffix\n          unit\n        }\n        county {\n          fips_code\n          name\n          state_code\n        }\n        search_areas {\n          city\n          state_code\n        }\n      }\n      photo_count\n      photos(limit: 3, https: true) {\n        description\n        href\n        type\n        title\n        tags {\n          label\n          probability\n        }\n      }\n      pet_policy {\n        cats\n        dogs\n        text\n      }\n      primary_photo(https: true) {\n        description\n        href\n        type\n      }\n      open_houses {\n        description\n        end_date\n        start_date\n        time_zone\n        dst\n      }\n      other_listings {\n        rdc {\n          listing_id\n          status\n          primary\n        }\n      }\n      products {\n        product_attributes\n        products\n      }\n      property_history {\n        listing {\n          photos {\n            href\n          }\n        }\n      }\n      property_id\n      source {\n        agents {\n          agent_id\n          agent_name\n        }\n        id\n        listing_id\n        community_id\n        name\n        type\n      }\n      status\n      suppression_flags\n      tags\n      when_indexed\n      source {\n        tier_rank\n        id\n      }\n      community_metrics {\n        leads_month_to_date\n        active_listing_count\n        community_price_per_lead\n      }\n    }\n    property_types: seo_linking_modules(type: top_property_types) {\n      title\n      linking_module {\n        title\n        url\n      }\n    }\n  }\n  meta\n}\n","variables":{"geoSupportedSlug":"","query":{"primary":true,"status":["for_rent"],"state_code":"OH","pending":false,"community_price_per_lead":{"min":0}},"limit":42,"offset":42,"bucket":{"sort":"rentalModelV2_1","sort_options":{"costar_total":0,"non_costar_total":0,"variation":"costar_basic"}},"sort":{"field":"community_price_per_lead","direction":"desc"}},"seoPayload":{"asPath":"/apartments/Ohio","pageType":{"silo":"search_result_page","status":"for_rent"},"county_needed_for_uniq":false}}'
        body = r'{"query":"\nquery ConsumerSearchQuery($query: HomeSearchCriteria!, $limit: Int, $offset: Int, $sort: [SearchAPISort], $bucket: SearchAPIBucket) {\n  home_search: home_search(query: $query, sort: $sort, limit: $limit, offset: $offset, bucket: $bucket) {\n    costar_counts {\n      costar_total\n      non_costar_total\n    }\n    count\n    total\n    aggregation\n    properties: results {\n      permalink\n      lead_attributes {\n        show_contact_an_agent\n      }\n      branding {\n        type\n        photo\n        name\n      }\n      price_reduced_date\n      price_reduced_amount\n      matterport\n      virtual_tours {\n        href\n      }\n      advertisers {\n        email\n        fulfillment_id\n        href\n        mls_set\n        name\n        nrds_id\n        office {\n          email\n          fulfillment_id\n          mls_set\n          href\n          name\n          phones {\n            ext\n            number\n            primary\n            trackable\n            type\n          }\n        }\n        phones {\n          ext\n          number\n          primary\n          trackable\n          type\n        }\n      }\n      description {\n        baths\n        baths_full\n        baths_full_calc\n        baths_half\n        baths_3qtr\n        baths_1qtr\n        beds\n        garage\n        lot_sqft\n        name\n        sqft\n        sub_type\n        type\n        year_built\n        baths_min\n        baths_max\n        beds_max\n        beds_min\n        garage_min\n        garage_max\n        sqft_max\n        sqft_min\n      }\n      flags {\n        is_pending\n        is_deal_available\n        is_for_rent\n        is_garage_present\n        is_senior_community\n        is_new_listing(days: 3)\n      }\n      href\n      last_price_change_amount\n      last_price_change_date\n      last_update_date\n      list_date\n      list_price\n      list_price_min\n      list_price_max\n      listing_id\n      location {\n        address {\n          city\n          coordinate {\n            lat\n            lon\n          }\n          country\n          line\n          postal_code\n          state\n          state_code\n          street_direction\n          street_name\n          street_number\n          street_post_direction\n          street_suffix\n          unit\n        }\n        county {\n          fips_code\n          name\n          state_code\n        }\n        search_areas {\n          city\n          state_code\n        }\n      }\n      photo_count\n      photos(limit: 3, https: true) {\n        description\n        href\n        type\n        title\n        tags {\n          label\n          probability\n        }\n      }\n      pet_policy {\n        cats\n        dogs\n        text\n      }\n      primary_photo(https: true) {\n        description\n        href\n        type\n      }\n      open_houses {\n        description\n        end_date\n        start_date\n        time_zone\n        dst\n      }\n      other_listings {\n        rdc {\n          listing_id\n          status\n          primary\n        }\n      }\n      products {\n        product_attributes\n        products\n      }\n      property_history {\n        listing {\n          photos {\n            href\n          }\n        }\n      }\n      property_id\n      source {\n        agents {\n          agent_id\n          agent_name\n        }\n        id\n        listing_id\n        community_id\n        name\n        type\n      }\n      status\n      suppression_flags\n      tags\n      when_indexed\n      source {\n        tier_rank\n        id\n      }\n      community_metrics {\n        leads_month_to_date\n        active_listing_count\n        community_price_per_lead\n      }\n    }\n    property_types: seo_linking_modules(type: top_property_types) {\n      title\n      linking_module {\n        title\n        url\n      }\n    }\n  }\n  meta\n}\n","variables":{"geoSupportedSlug":"","query":{"primary":true,"status":["for_rent"],"state_code":"FL","pending":false,"community_price_per_lead":{"min":0}},"limit":42,"offset":42,"bucket":{"sort":"rentalModelV2_1","sort_options":{"costar_total":0,"non_costar_total":0,"variation":"costar_basic"}},"sort":{"field":"community_price_per_lead","direction":"desc"}},"seoPayload":{"asPath":"/apartments/Florida","pageType":{"silo":"search_result_page","status":"for_rent"},"county_needed_for_uniq":false}}'
        json_body = json.loads(body)

        json_body["variables"]["page_index"] = page_number
        json_body["seoPayload"] = page_number
        json_body["variables"]["offset"] = offset_parameter

        r = requests.post(url=url, json=json_body, headers=headers)
        json_data = r.json()
        return json_data

    def extract_features(self, entry: dict) -> dict:
        pict = [i['href'] for i in entry["photos"]]
        feature_dict = {
            "id": entry["property_id"],
            "price": entry["list_price"],
            "min_price": entry["list_price_min"],
            "max_price": entry["list_price_max"],
            'cats': entry["pet_policy"].get('cats'),
            'dogs': entry["pet_policy"].get('dogs'),
            'pet_policy_text': entry["pet_policy"].get('text'),
            "beds": entry["description"]["beds"],
            "min_beds": entry["description"]["beds_min"],
            "max_beds": entry["description"]["beds_max"],
            "baths": entry["description"]["baths"],
            "min_baths": entry["description"]["baths_min"],
            "max_baths": entry["description"]["baths_max"],
            "garage": entry["description"]["garage"],
            # "stories": entry["description"]["stories"],
            "house_type": entry["description"]["type"],
            # "lot_sqft": entry["description"]["lot_sqft"],
            "sqft": entry["description"]["sqft"],
            "year_built": entry["description"]["year_built"],
            "address": entry["location"]["address"]["line"],
            "postal_code": entry["location"]["address"]["postal_code"],
            "state": entry["location"]["address"]["state_code"],
            "city": entry["location"]["address"]["city"],
            # "tags": entry["tags"],
            "pictures": pict[0],
            "pictures1": pict[1]
        }

        if entry["location"]["address"]["coordinate"]:
            feature_dict.update({"lat": entry["location"]["address"]["coordinate"]["lat"]})
            feature_dict.update({"lon": entry["location"]["address"]["coordinate"]["lon"]})

        if entry["location"]["county"]:
            feature_dict.update({"county": entry["location"]["county"]["name"]})

        return feature_dict

    def parse_json_data(self) -> list:
        offset_parameter = 500

        feature_dict_list = []

        for i in range(self.page_numbers):
            json_data = self.send_request(page_number=i + 1, offset_parameter=offset_parameter)
            # offset_parameter += 42
            print(i)

            try:
                for entry in json_data["data"]["home_search"]["properties"]:
                    feature_dict = self.extract_features(entry)
                    feature_dict_list.append(feature_dict)
            except:
                pass

        return feature_dict_list

    def create_dataframe(self) -> pd.DataFrame:
        feature_dict_list = self.parse_json_data()

        df = pd.DataFrame(feature_dict_list)
        # dummy_df = pd.get_dummies(df['tags'].explode()).groupby(level=0).sum()
        #
        # merged_df = pd.merge(df, dummy_df, left_index=True, right_index=True)
        return df


if __name__ == "__main__":
    r = RealtorScraper(page_numbers=10)
    # pprint(r.send_request(1, 42))
    df = r.create_dataframe()
    print(df)
    # df.to_csv('Florida.csv', index=False)
    # print(tabulate(df, headers=df.columns))
