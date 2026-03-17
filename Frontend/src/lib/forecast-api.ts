export type BackendForecastRow = {
  "Date-Hour": string;
  "PredictedSolarPower": number;
};

export type Insight = {
  title: string;
  description: string;
  detail: string;
  icon: string;
};

export type ForecastResponse = {
  forecast: BackendForecastRow[];
  insights: Insight[];   // ✅ ADDED
};

export async function fetchSolarForecast(): Promise<ForecastResponse> {
  const res = await fetch("/api/solar-forecast");
  if (!res.ok) throw new Error("Forecast fetch failed");
  return (await res.json()) as ForecastResponse;
}