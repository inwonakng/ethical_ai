from django import forms

class VotingSimForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    no_candidates = forms.IntegerField(label='Number of Candidates')
    group_sizes = forms.CharField(label='Group Sizes')
    sim_data_size = forms.IntegerField(label='Simluated Data Size')
    conc_eff_req = forms.FloatField(label='Condorcet Efficiency Requirement')
    gr_fair_req = forms.FloatField(label='Group Fairness Requirement')
    privacy = forms.FloatField(label='privacy')