from pathlib import Path


resource_dir = Path(__file__).absolute().parent / 'resources/'
admin_path = Path(__file__).absolute().parent / 'admin'

candidates_file = resource_dir / 'candidates.pkl'
user_votes_file = resource_dir / 'user_votes.pkl'
