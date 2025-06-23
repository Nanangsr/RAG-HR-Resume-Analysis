// src/utils/export.js
function convertToCSV(rankingData, criteria) {
    const headers = ["Ranking", "Nama", "Level", "Skor AI", ...Object.keys(criteria)];
    const rows = rankingData.map(candidate => {
        const row = [
            candidate.rank,
            `"${candidate.name.replace(/"/g, '""')}"`, // Handle names with quotes
            candidate.level,
            candidate.ai_score,
            ...Object.keys(criteria).map(key => candidate.scores[key] || 'N/A')
        ];
        return row.join(',');
    });
    return [headers.join(','), ...rows].join('\n');
}

export function exportToCSV(results) {
    if (!results || !results.ranking) return;
    const csvString = convertToCSV(results.ranking, results.criteria);
    const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", "candidate_analysis.csv");
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

export function exportToJSON(results) {
    if (!results) return;
    const jsonString = `data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify(results, null, 2))}`;
    const link = document.createElement("a");
    link.setAttribute("href", jsonString);
    link.setAttribute("download", "candidate_analysis.json");
    link.click();
}