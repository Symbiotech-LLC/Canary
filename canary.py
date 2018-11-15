from src.main import Canary
from src.base.get_arguments import get_arguments
import multiprocessing, platform, os


if __name__ == '__main__':
	# Change environment variable to allow multiprocessing
	if platform.system() == 'Darwin':
		try:
			if not 'OBJC_DISABLE_INITIALIZE_FORK_SAFETY' in os.environ:
				os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
		except Exception as e:
			print(e)
			print("If you experience errors when executing, Set the environment variable to allow multiprocessing:")
			print("to set in bash: 'export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES'")
			pass
	multiprocessing.freeze_support()
	arguments = get_arguments()
	Canary(arguments)
