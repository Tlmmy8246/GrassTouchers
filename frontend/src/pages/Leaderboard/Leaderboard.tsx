import { useState } from "react";
import { useFetchLeaderboard } from "api/leaderboard/useLeaderboard";

type TQueryState = 'messages' | 'credits';

const Leaderboard = () => {
  const [queryState, setQueryState] = useState<TQueryState>('messages');

  const {data} = useFetchLeaderboard({
    query: queryState
  });

  // Example users array
  const users = [
    { name: "Alfreds Futterkiste", socialCredit: 120 },
    { name: "Centro comercial", socialCredit: 95 },
    { name: "Maria Anders", socialCredit: 85 },
  ];

  return (
    <>
      <h1>Leaderboard</h1>
      <table>
        <thead>
          <tr>
            <th>User</th>
            <th>Anti-Social Credit</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user, index) => (
            <tr key={index}>
              <td>{user.name}</td>
              <td>{user.socialCredit}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
};

export default Leaderboard;
