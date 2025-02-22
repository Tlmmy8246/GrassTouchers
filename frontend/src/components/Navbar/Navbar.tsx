import { Button } from "components";
import tropy from 'assets/tropy.svg';
import useMediaQuery from "hooks/useMediaQuery";
import { useNavigate } from "react-router";
import { routePaths } from "global/routePaths";
import tokenService from "utils/token";

const Navbar = () => {
	const isMobile = useMediaQuery("(max-width: 768px)");
	const navigate = useNavigate();

	const handleLeaderboardClick = () => {
		navigate(routePaths.leaderboard);
	}

	const handleSlowGrowthClick = () => {
		// TODO: Implement slow growth
	}

	const handleRemoveAllClick = () => {
		// TODO: Implement remove all
	}

	const handleSendAllClick = () => {
		// TODO: Implement send all
	}

	const handleLogout = () => {
		tokenService.clearToken();
		navigate(routePaths.auth.login);
	}

	return (
		<nav>
			<div className="mx-auto flex flex-wrap gap-3 justify-center items-center p-2" >
				<Button className="min-w-fit whitespace-normal w-fit" title="Leaderboard" onClick={handleLeaderboardClick}>
					<img src={tropy} alt="Tropy" className="w-6 h-6" />
				</Button>
				<div className="p-2 w-fit bg-gray-300/60 border-black border-3 text-green-800 whitespace-nowrap truncate md:w-full">
					{isMobile ? '$ 10000' : '$ 10000 gbucks'}
				</div>
				<Button className="w-fit md:w-full" onClick={handleSlowGrowthClick}>
					Slow Growth
				</Button>
				<Button className="w-fit md:w-full" onClick={handleRemoveAllClick}>
					Remove All
				</Button>
				<Button className="w-fit md:w-full" onClick={handleSendAllClick}>
					Send All
				</Button>
				<Button className="w-fit md:w-full" onClick={handleLogout}>
					Logout
				</Button>
			</div>
		</nav>
	)
}

export default Navbar
