# Importing required libraries
import sys
sys.path.append('/PERSONAL DATA/python/Online Compitions/Job Test/AbsentiaVR/env/Lib/site-packages') # Replace this with the place you installed facebookads using pip
sys.path.append('/PERSONAL DATA/python/Online Compitions/Job Test/AbsentiaVR/env/Lib/site-packages/facebook_business-3.0.0-py2.7.egg-info') # same as above

# For Campaign
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign

# For Adset
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.targeting import Targeting

# For Ad Creatives
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebook_business.adobjects.adcreativeobjectstoryspec \
    import AdCreativeObjectStorySpec

# For Image Hash
from facebook_business.adobjects.adimage import AdImage

# For Ad
from facebook_business.adobjects.ad import Ad

#For initiaslization
from facebook_business.api import FacebookAdsApi

#For GET AND POST REQUESTS
import requests as re


# Class to create, delete and update
class CampaignCreationAPI():
    # Here Initializing done.
    def __init__(self, access_token, app_secret, app_id, id):
        self.access_token = access_token
        self.app_secret = app_secret
        self.app_id = app_id
        self.id = id
        FacebookAdsApi.init(access_token=self.access_token)

    def createCampaign(self, name):
        print("**Creating {} Campaign...**".format(name))
        campaign = Campaign()
        campaign['_parent_id'] = self.id
        campaign[Campaign.Field.name] = name
        campaign[Campaign.Field.objective] = 'LINK_CLICKS'
        campaign[Campaign.Field.status] = 'PAUSED'
        campaign.remote_create()
        self.campaign_id = str(campaign[Campaign.Field.id])
        print("**Campaign ID: {}**".format(self.campaign_id))
        return campaign

    def createAdSet(self, name):
        print("**Creating {} Ad Set...**".format(name))
        targeting_object ={Targeting.Field.geo_locations: {'countries': ['IN'],}}
        adset = AdSet()
        adset['_parent_id'] = self.id
        adset.update({
            AdSet.Field.name: name,
            AdSet.Field.campaign_id: self.campaign_id,
            AdSet.Field.lifetime_budget: 80 * 10000,
            AdSet.Field.bid_strategy: 'LOWEST_COST_WITHOUT_CAP',
            AdSet.Field.billing_event: AdSet.BillingEvent.impressions,
            AdSet.Field.optimization_goal: AdSet.OptimizationGoal.reach,
            AdSet.Field.targeting: targeting_object,
            AdSet.Field.start_time: '2019-02-01 00:00:00',
            AdSet.Field.end_time: '2019-02-30 23:59:00',
            AdSet.Field.status: AdSet.Status.paused,
        })
        adset.remote_create()
        self.adset_id = str(adset[AdSet.Field.id])
        print("**AdSet ID: {}**".format(self.adset_id))
        return adset

    def createAd(self, name):
        print("Creating Image Hash...")
        img_path = 'Icon-1024.png'
        image = AdImage()
        image['_parent_id'] = id
        image[AdImage.Field.filename] = img_path
        image.remote_create()

        print("**Image Hash...**")
        # Output image Hash
        image_hash = image[AdImage.Field.hash]
        ##image_hash = "5c2f70590d5a1381f1871a5e3731ecb1"
        print("**Image Hash : {}**".format(image_hash))
        

                
        print("** Creating Ad Creative...**")
        website_url = "www.example.com"
        page_id = '181951488809425'
        link_data = AdCreativeLinkData()
        link_data[AdCreativeLinkData.Field.name] = 'main text 001'
        link_data[AdCreativeLinkData.Field.message] = 'title 001'
        link_data[AdCreativeLinkData.Field.link] = website_url
        link_data[AdCreativeLinkData.Field.image_hash] = image_hash

        object_story_spec = AdCreativeObjectStorySpec()
        object_story_spec[AdCreativeObjectStorySpec.Field.page_id] = page_id
        object_story_spec[AdCreativeObjectStorySpec.Field.link_data] = link_data

        creative = AdCreative()
        creative['_parent_id'] = id
        creative[AdCreative.Field.object_story_spec] = object_story_spec
        creative[AdCreative.Field.title] = 'Main text 001'
        creative[AdCreative.Field.body] = 'Title 001'
        creative[AdCreative.Field.actor_id] = page_id
        creative[AdCreative.Field.link_url] = website_url
        creative[AdCreative.Field.object_type] = AdCreative.ObjectType.domain
        creative[AdCreative.Field.image_hash] = image_hash
        print("Ad Creative created successfully!")


        print("***Ad...*")
        ad = Ad()
        ad['_parent_id'] = self.id
        ad[Ad.Field.name] = name
        ad[Ad.Field.adset_id] = self.adset_id
        ad[Ad.Field.creative] = creative
        ad.remote_create(params={
            'status': Ad.Status.paused,
        })
        self.ad_id = str(ad[Ad.Field.id])
        print("**Ad ID: {}**".format(self.ad_id))
        return ad

    def campaign_status_update(self, campaign_id):
        try:
            campaign = Campaign(campaign_id)
            campaign[Campaign.Field.status] = 'ACTIVE'
            campaign.remote_update()
            print("Sucussfully Campaign updated!")
        except Exception as e:
            print(e)

    def adset_status_update(self, adset_id):
        try:
            adset = AdSet(fbid=adset_id)
            adset.update({
                AdSet.Field.status: AdSet.Status.active,
            })
            adset.remote_update()
            print("Successfully AdSet updated!")
        except Exception as e:
            print(e)
    
    def ad_status_update(self, ad_id):
        try:
            ad = Ad(ad_id)
            ad[Ad.Field.status] = 'ACTIVE'
            ad.remote_update()
            print("Successfully Ad updated!")
        except Exception as e:
            print(e)

    def campaign_delete(self, campaign_id):
        campaign = Campaign(campaign_id)
        campaign.remote_delete()
        print("Sucussfully Campaign deleted!")

    def adset_delete(self, adset_id):
        adset = AdSet(adset_id)
        adset.remote_delete()
        print("Sucussfully Ad Set deleted!")

    def ad_delete(self, ad_id):
        ad = Ad(ad_id)
        ad.remote_delete()
        print("Sucussfully Ad deleted!")




if __name__ == "__main__" :
    access_token = 'EAACcz9Hkm2EBAJs0R8p8MUNddpU2HoFLq2U2CrBoZApj5DUGG3TzZBbTXMRYFi8P2xLhVrvzeVi1nR4DqN94Nz1dZBHACVRHZAgSro99O5g6qSPTB9htHvUFZCpnDd1aiGer8wZCIEU0kNtrL4AY28H1yd1m9sx0eI1GeZAQtRFVAZDZD'
    app_secret = 'f8c7f721cc3585c6966581745dd23cba'
    app_id = '172416393583457'
    id = 'act_185949559'
    c = CampaignCreationAPI(access_token, app_secret, app_id, id)

    while True:
        
        print("Welcome to Campaign Creation API!")
        q1 = input("Want to create Capmapign: (Y/N/Q)? \n")
        if q1.lower() == 'y':
            c_name = str(input("Enter the Campaign name: "))
            if c_name:
                campaign = c.createCampaign(c_name)
            
            as_name = str(input("Enter the Ad Set name: "))
            if as_name:
                adset = c.createAdSet(as_name)
            
            ad_name = str(input("Enter the Ad name: "))
            if ad_name:
                ad = c.createAd(ad_name)
        elif q1.lower() == 'n':
            pass
        elif q1.lower() == 'q':
            break
                
        q2 = input("Want to update Capmapign/AdSet/Ad: (Y/N/Q)? \n")
        if q2.lower() == 'y':

            c_id = str(input("Enter the Campaign ID: "))
            if c_id:
                campaign = c.campaign_status_update(c_id)
                
            as_id = str(input("Enter the AdSet ID: "))
            if as_id:
                adset = c.adset_status_update(as_id)

            a_id = str(input("Enter the Ad ID: "))
            if a_id:
                ad = c.ad_status_update(a_id)
        elif q2.lower() == 'n':
            pass
        elif q2.lower() == 'q':
            break

        q3 = input("Want to delete Capmapign/AdSet/Ad: (Y/N/Q)? \n")
        if q3.lower() == 'y':

            a_id = str(input("Enter the Ad ID: "))
            if a_id:
                ad = c.ad_delete(a_id)
            
            as_id = str(input("Enter the AdSet ID: "))
            if as_id:
                adset = c.adset_delete(as_id)

            c_id = str(input("Enter the Campaign ID: "))
            if c_id:
                campaign = c.campaign_delete(c_id)

            
        elif q3.lower() == 'n':
            pass
        elif q3.lower() == 'q':
            break

        
        
        
