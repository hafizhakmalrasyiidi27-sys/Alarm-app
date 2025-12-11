import React from "react";
import { BarChart, TrendingUp, Moon, Award } from "lucide-react";

interface SleepLogEntry {
  id: string;
  date: string;
  duration: number; 
  quality?: number | null;
}

interface Props {
  logs: SleepLogEntry[];
}

export default function SleepStats({ logs }: Props) {
  if (!logs || logs.length === 0) {
    return (
      <div className="text-center text-gray-500 py-10">
        Belum ada data tidur.
      </div>
    );
  }

  const durations = logs.map((l) => l.duration);
  const qualities = logs.map((l) => l.quality).filter((q) => q != null) as number[];

  const avgSleep = durations.reduce((a, b) => a + b, 0) / durations.length;
  const avgHours = Math.floor(avgSleep / 60);
  const avgMinutes = Math.floor(avgSleep % 60);

  const avgQuality = qualities.length > 0 
    ? qualities.reduce((a, b) => a + b, 0) / qualities.length 
    : 0;

  const longest = Math.max(...durations);
  const shortest = Math.min(...durations);

  const mean = avgSleep;
  const variance = durations.reduce((sum, d) => sum + Math.pow(d - mean, 2), 0) / durations.length;
  const stddev = Math.sqrt(variance);
  const consistency = Math.max(0, Math.min(100, 100 - (stddev / 60) * 10));

  const last7 = logs.slice(-7);

  function formatDuration(min: number) {
    const h = Math.floor(min / 60);
    const m = min % 60;
    return `${h}j ${m}m`;
  }

  return (
    <div className="w-full max-w-2xl mx-auto py-6 px-4 font-sans">
      <div className="relative">
        <img
          src="/sleep-banner.jpg"
          className="w-full h-44 object-cover rounded-xl"
        />

        <div className="absolute bottom-3 left-4 bg-black bg-opacity-40 px-4 py-2 rounded-lg backdrop-blur-sm">
          <h2 className="text-white text-xl font-semibold">Statistik Tidur</h2>
          <p className="text-gray-200 text-sm">Analisis 7 hari terakhir</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mt-5">
        {/* Average Sleep */}
        <div className="bg-white rounded-xl p-4 shadow-md border flex flex-col">
          <div className="flex items-center gap-2 text-gray-700">
            <Moon size={18} />
            <span className="font-medium">Rata-rata Tidur</span>
          </div>
          <p className="text-2xl font-bold mt-1">{avgHours}j {avgMinutes}m</p>
          <p className="text-sm text-gray-500">per malam</p>
        </div>

        {/* Quality */}
        <div className="bg-white rounded-xl p-4 shadow-md border flex flex-col">
          <div className="flex items-center gap-2 text-gray-700">
            <Award size={18} />
            <span className="font-medium">Kualitas</span>
          </div>
          <p className="text-2xl font-bold mt-1">{avgQuality.toFixed(1)}</p>
          <p className="text-sm text-gray-500">skala 1 - 5</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mt-5">
        <div className="bg-white rounded-xl p-4 shadow-md border">
          <p className="font-medium text-gray-700">Terpanjang</p>
          <p className="text-xl font-bold mt-2">{formatDuration(longest)}</p>
        </div>

        <div className="bg-white rounded-xl p-4 shadow-md border">
          <p className="font-medium text-gray-700">Tersingkat</p>
          <p className="text-xl font-bold mt-2">{formatDuration(shortest)}</p>
        </div>
      </div>

      <div className="mt-5 bg-white rounded-xl p-4 shadow-md border">
        <div className="flex items-center gap-2 text-gray-700 mb-2">
          <TrendingUp size={18} />
          <span className="font-medium">Konsistensi</span>
        </div>
        <p className="text-xl font-bold">{consistency.toFixed(0)}%</p>
      </div>

      {/* Trend 7 days */}
      <div className="mt-6 bg-white rounded-xl p-4 shadow-md border">
        <div className="flex items-center gap-2 text-gray-700 mb-3">
          <BarChart size={18} />
          <span className="font-medium">Tren 7 Hari</span>
        </div>

        <div className="space-y-3">
          {last7.map((log) => {
            const percent = Math.min(100, Math.round((log.duration / 480) * 100));
            const date = new Date(log.date).toLocaleDateString("id-ID", {
              day: "2-digit",
              month: "short",
            });

            return (
              <div key={log.id}>
                <p className="text-sm font-medium text-gray-700">
                  {date} — {formatDuration(log.duration)}
                </p>
                <div className="w-full bg-gray-200 h-3 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-500 rounded-full"
                    style={{ width: `${percent}%` }}
                  ></div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <p className="text-center text-gray-500 text-sm mt-6">
        Idealnya tidur 7–9 jam setiap malam.
      </p>
    </div>
  );
}
