from project.campaigns.high_budget_campaign import HighBudgetCampaign
from project.campaigns.low_budget_campaign import LowBudgetCampaign
from project.influencers.premium_influencer import PremiumInfluencer
from project.influencers.standard_influencer import StandardInfluencer


class InfluencerManagerApp:

    CAMPAIGN_TYPES = {"HighBudgetCampaign": HighBudgetCampaign, "LowBudgetCampaign": LowBudgetCampaign}
    INFLUENCER_TYPES = {"PremiumInfluencer": PremiumInfluencer, "StandardInfluencer": StandardInfluencer}

    def __init__(self):
        self.influencers = []
        self.campaigns = []

    def _influencer_in_list(self, username: str):
        matches = [i for i in self.influencers if i.username == username]
        return True if matches else False

    def _campaign_in_list(self, campaign_id: int):
        matches = [c for c in self.campaigns if c.campaign_id == campaign_id]
        return True if matches else False

    def _find_campaign(self, campaign_id: int):
        matches = [c for c in self.campaigns if c.campaign_id == campaign_id]
        return matches[0] if matches else None

    def _find_influencer(self, username: str):
        matches = [i for i in self.influencers if i.username == username]
        return matches[0] if matches else None

    def register_influencer(self, influencer_type: str, username: str, followers: int, engagement_rate: float):
        if influencer_type not in self.INFLUENCER_TYPES:
            return f"{influencer_type} is not an allowed influencer type."
        if self._influencer_in_list(username):
            return f"{username} is already registered."
        influencer = self.INFLUENCER_TYPES[influencer_type](username, followers, engagement_rate)
        self.influencers.append(influencer)
        return f"{username} is successfully registered as a {influencer_type}."

    def create_campaign(self, campaign_type: str, campaign_id: int, brand: str, required_engagement: float):
        if campaign_type not in self.CAMPAIGN_TYPES:
            return f"{campaign_type} is not a valid campaign type."
        if self._campaign_in_list(campaign_id):
            return f"Campaign ID {campaign_id} has already been created."
        campaign = self.CAMPAIGN_TYPES[campaign_type](campaign_id, brand, required_engagement)
        self.campaigns.append(campaign)
        return f"Campaign ID {campaign_id} for {brand} is successfully created as a {campaign_type}."

    def participate_in_campaign(self, influencer_username: str, campaign_id: int):
        influencer = self._find_influencer(influencer_username)
        if influencer is None:
            return f"Influencer '{influencer_username}' not found."
        campaign = self._find_campaign(campaign_id)
        if campaign is None:
            return f"Campaign with ID {campaign_id} not found."
        if not campaign.check_eligibility(influencer.engagement_rate):
            return f"Influencer '{influencer_username}' does not meet the eligibility criteria for the campaign with ID {campaign_id}."
        payment = influencer.calculate_payment(campaign)
        if payment > 0.0:
            campaign.approved_influencers.append(influencer)
            campaign.budget -= payment
            influencer.campaigns_participated.append(campaign)
            return f"Influencer '{influencer_username}' has successfully participated in the campaign with ID {campaign_id}."

    def calculate_total_reached_followers(self):
        total_followers = {}
        for campaign in self.campaigns:
            if campaign.approved_influencers:
                total_followers[campaign] = 0
                for influencer in campaign.approved_influencers:
                    if campaign in influencer.campaigns_participated:
                        total_followers[campaign] += influencer.reached_followers(campaign.__class__.__name__)
        return total_followers

    def influencer_campaign_report(self, username: str):
        influencer = self._find_influencer(username)
        if influencer is not None:
            return influencer.display_campaigns_participated()

    def campaign_statistics(self):
        campaigns_sorted = sorted(self.campaigns, key=lambda c: (len(c.approved_influencers), -c.budget))
        statistics = ["$$ Campaign Statistics $$"]
        for campaign in campaigns_sorted:
            total_followers = self.calculate_total_reached_followers()
            total_campaign_followers = total_followers[campaign]
            statistics.append(f"  * Brand: {campaign.brand}, Total influencers: {len(campaign.approved_influencers)}, "
                              f"Total budget: ${campaign.budget:.2f}, "
                              f"Total reached followers: {total_campaign_followers}")
        return "\n".join(statistics)
