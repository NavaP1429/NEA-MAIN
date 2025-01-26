// DOM elements
const leagueDropdown = document.getElementById('league'); // League dropdown
const teamDropdown = document.getElementById('team'); // Team dropdown
const proceedButton = document.getElementById('proceed'); // Proceed button
const mainPage = document.getElementById('main-page');

// API Key and Headers
const API_KEY = '9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284';
const API_HOST = 'api-football-v1.p.rapidapi.com';

// Declare the variable globally
let leagueId; // This will hold the selected league ID

// Fetch leagues and populate dropdown
fetch(`/static/leagues.json`, {
  method: 'GET',
})
  .then((response) => response.json())
  .then((data) => {
    // Populate leagues dropdown
    data.response.forEach((league) => {
      const option = document.createElement('option');
      option.value = league.league.id; // League ID as value
      option.textContent = `${league.league.name} (${league.country.name})`; // Display name
      leagueDropdown.appendChild(option);
    });
  })
  .catch((err) => console.error('Error fetching leagues:', err));

// Event listener for league selection to fetch teams
leagueDropdown.addEventListener('change', () => {
  leagueId = leagueDropdown.value; // Get selected league ID
  teamDropdown.innerHTML = '<option value="">Select a team</option>'; // Clear previous options

  if (leagueId) {
    // Fetch teams for selected league
    fetch(`https://api-football-v1.p.rapidapi.com/v3/teams?league=${leagueId}&season=2024`, {
      method: 'GET',
      headers: {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        data.response.forEach((team) => {
          const option = document.createElement('option');
          option.value = team.team.id; // Team ID as value
          option.textContent = team.team.name; // Display team name
          teamDropdown.appendChild(option);
        });
      })
      .catch((err) => console.error('Error fetching teams:', err));
  }
});

// Event listener for Proceed button
proceedButton.addEventListener('click', () => {
  leagueId = leagueDropdown.value;
  const teamId = teamDropdown.value;

  if (!leagueId) {
    alert('Please select a league!');
    return;
  }
// Redirect to a new page with the selected league ID and team ID
if (teamId) {
  // If both leagueId and teamId are selected, include both in the query string
  window.location.href = `teamfixtures.html?leagueId=${leagueId}&teamId=${teamId}`;
} else {
  // If only leagueId is selected, include just the leagueId
  window.location.href = `leaguefixtures.html?leagueId=${leagueId}`;
}
});

document.addEventListener('DOMContentLoaded', () => {
  // Function to get query parameters
  function getQueryParams() {
    const params = {};
    const queryString = window.location.search.substring(1);
    const regex = /([^&=]+)=([^&]*)/g;
    let m;

    while ((m = regex.exec(queryString))) {
      params[decodeURIComponent(m[1])] = decodeURIComponent(m[2]);
    }
    return params;
  }

  // Get leagueId from query parameters
  const params = getQueryParams();
  const leagueId = params.leagueId; // Capture leagueId dynamically

  // Function to load fixtures from the API
  function loadFixtures(leagueId) {
    const season = 2024; // Set the season (can be dynamic if needed)

    

    // Fetch fixtures for the selected league from the API
    fetch(`https://api-football-v1.p.rapidapi.com/v3/fixtures?league=${leagueId}&season=${season}`, {
      method: 'GET',
      headers: {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        const fixturesContainer = document.getElementById('fixtures-container');
        const leagueNameElement = document.getElementById('league-name');
        fixturesContainer.innerHTML = ''; // Clear existing content
        // Set the league logo
        const leagueLogoElement = document.getElementById('league-logo'); 
        const leagueLogo = data.response[0].league.logo; // League logo URL
        leagueLogoElement.src = leagueLogo; // Set logo source
        leagueLogoElement.alt = `${leagueId} logo`; // Set alt text for the logo

        if (data.response && data.response.length > 0) {
          // Set the league name
          const leagueName = data.response[0].league.name;
          leagueNameElement.textContent = leagueName;

          // Group fixtures by date
          const fixturesByDate = {};
          data.response.forEach((fixture) => {
            const fixtureDate = new Date(fixture.fixture.date).toLocaleDateString();
            const homeTeam = fixture.teams.home.name;
            const awayTeam = fixture.teams.away.name;
            const homeScore = fixture.goals.home;
            const awayScore = fixture.goals.away;
            const status = fixture.fixture.status.short; // Status: "FT" (Full-Time), "NS" (Not Started)
            const time = new Date(fixture.fixture.date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

            if (!fixturesByDate[fixtureDate]) {
              fixturesByDate[fixtureDate] = [];
            }

            // Display scores if the fixture has already taken place
            const matchResult =
              status === 'FT'
                ? `${homeTeam} ${homeScore} - ${awayScore} ${awayTeam}`
                : `${homeTeam} (${time}) vs ${awayTeam}`;

            fixturesByDate[fixtureDate].push(matchResult);
          });

          // Render fixtures grouped by date
          Object.keys(fixturesByDate).forEach((date) => {
            const dateSection = document.createElement('div');
            dateSection.className = 'fixture-date';

            const dateTitle = document.createElement('h3');
            dateTitle.textContent = `Date: ${date}`;
            dateSection.appendChild(dateTitle);

            fixturesByDate[date].forEach((fixture) => {
              const fixtureElement = document.createElement('div');
              fixtureElement.className = 'fixture';
              fixtureElement.textContent = fixture;
              dateSection.appendChild(fixtureElement);
            });

            fixturesContainer.appendChild(dateSection);
          });
        } else {
          fixturesContainer.textContent = 'No fixtures found for this league.';
        }
      })
      .catch((err) => {
        console.error('Error fetching fixtures:', err);
        const fixturesContainer = document.getElementById('fixtures-container');
        fixturesContainer.textContent = 'An error occurred while fetching fixtures.';
      });
  }

  // Load fixtures when the page loads
  if (leagueId) {
    loadFixtures(leagueId);
  } else {
    const fixturesContainer = document.getElementById('fixtures-container');
    fixturesContainer.textContent = 'League ID is missing.';
  }
});
document.addEventListener("DOMContentLoaded", () => {
  // Function to get query parameters
  function getQueryParams() {
    const params = {};
    const queryString = window.location.search.substring(1);
    const regex = /([^&=]+)=([^&]*)/g;
    let match;

    while ((match = regex.exec(queryString))) {
      params[decodeURIComponent(match[1])] = decodeURIComponent(match[2]);
    }
    return params;
  }

  const params = getQueryParams();
  const leagueId = params.leagueId; // Get leagueId from the query parameter
  const teamId = params.teamId; // Get teamId from the query parameter
  const API_KEY = "9d75d9a7d5mshdce0c5c31b4e8abp113de0jsna22a3bb6d284";
  const API_HOST = "api-football-v1.p.rapidapi.com";
  const season = 2024;
 
  function loadTeamName(teamId) {
    const teamNameElement = document.getElementById("team-name");
  
    // Fetch team information
    fetch(
      `https://api-football-v1.p.rapidapi.com/v3/teams?id=${teamId}`,
      {
        method: "GET",
        headers: {
          "x-rapidapi-key": API_KEY,
          "x-rapidapi-host": API_HOST,
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error fetching team name: ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data.response && data.response.length > 0) {
          const teamName = data.response[0].team.name;
          teamNameElement.textContent = `Team: ${teamName}`;
        } else {
          teamNameElement.textContent = "Team: Unknown";
        }
      })
      .catch((err) => {
        console.error(err);
        teamNameElement.textContent = "Team: Error loading name";
      });
  }
  
  // Function to load fixtures from the API
  function loadFixtures(leagueId, teamId) {
    const fixturesContainer = document.getElementById("fixtures-container");
    const leagueNameElement = document.getElementById("league-name");
    // Set the league logo
    const leagueLogoElement = document.getElementById('league-logo'); // Ensure you add this element in your HTML
    const leagueLogo = data.response[0].league.logo; // League logo URL
    leagueLogoElement.src = leagueLogo; // Set logo source
    leagueLogoElement.alt = `${leagueName} logo`; // Set alt text for the logo

    // Ensure both leagueId and teamId are provided
    if (!leagueId || !teamId) {
      fixturesContainer.textContent = "League ID or Team ID is missing from the URL.";
      return;
    }

    // Fetch fixtures filtered by leagueId and teamId
    fetch(
      `https://api-football-v1.p.rapidapi.com/v3/fixtures?league=${leagueId}&season=${season}&team=${teamId}`,
      {
        method: "GET",
        headers: {
          "x-rapidapi-key": API_KEY,
          "x-rapidapi-host": API_HOST,
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Error fetching fixtures: ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        fixturesContainer.innerHTML = ""; // Clear loading text

        if (data.response && data.response.length > 0) {
          const fixturesByDate = {};
          const leagueName = data.response[0].league.name;
          leagueNameElement.textContent = `League: ${leagueName}`;

          // Group fixtures by date
          data.response.forEach((fixture) => {
            const fixtureDate = new Date(fixture.fixture.date).toLocaleDateString();
            const homeTeam = fixture.teams.home.name;
            const awayTeam = fixture.teams.away.name;
            const status = fixture.fixture.status.short;
            const time = new Date(fixture.fixture.date).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            });

            if (!fixturesByDate[fixtureDate]) {
              fixturesByDate[fixtureDate] = [];
            }
            // Generate match display format with team logos
            const homeTeamLogo = fixture.teams.home.logo; // Home team logo URL
            const awayTeamLogo = fixture.teams.away.logo; // Away team logo URL
            // Generate match display format
            const matchDisplay =
              status === "FT"
              ? `<img src="${homeTeamLogo}" alt="${homeTeam} logo" class="team-logo">
              ${homeTeam} ${fixture.goals.home} - ${fixture.goals.away} ${awayTeam}
              <img src="${awayTeamLogo}" alt="${awayTeam} logo" class="team-logo">`
           : `<img src="${homeTeamLogo}" alt="${homeTeam} logo" class="team-logo">
              ${homeTeam} (${time}) vs ${awayTeam}
              <img src="${awayTeamLogo}" alt="${awayTeam} logo" class="team-logo">`;

            fixturesByDate[fixtureDate].push(matchDisplay);
          });

          // Render fixtures grouped by date
          Object.keys(fixturesByDate).forEach((date) => {
            const dateSection = document.createElement("div");
            dateSection.className = "fixture-date";

            const dateTitle = document.createElement("h3");
            dateTitle.textContent = date;
            dateSection.appendChild(dateTitle);

            fixturesByDate[date].forEach((fixture) => {
              const fixtureElement = document.createElement("div");
              fixtureElement.className = "fixture";
              fixtureElement.textContent = fixture;
              dateSection.appendChild(fixtureElement);
            });

            fixturesContainer.appendChild(dateSection);
          });
        } else {
          fixturesContainer.textContent = "No fixtures found for this team in the selected league.";
        }
      })
      .catch((err) => {
        console.error(err);
        fixturesContainer.textContent = "An error occurred while loading fixtures.";
      });
  }

  // Load fixtures for the selected league and team
  loadFixtures(leagueId, teamId);
  loadTeamName(teamId);
});

