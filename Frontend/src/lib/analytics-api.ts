export type AnalyticsResponse = {
  average_production: number;
  average_radiation: number;
  correlation_radiation_production: number;
  radiation_vs_production: { Radiation: number; PredictedSolarPower: number }[];
  temperature_vs_production: { AirTemperature: number; PredictedSolarPower: number }[];
  solar_production_trends: { date: string; PredictedSolarPower: number }[];
  heatmap: { date: string; hour: number; PredictedSolarPower: number }[];
};

export async function fetchAnalytics() {
  const res = await fetch("/api/analytics");
  if (!res.ok) throw new Error("Analytics fetch failed");
  return (await res.json()) as AnalyticsResponse;
}
