import { BarChart, TrendingUp, Moon, Award } from 'lucide-react';
import type { SleepLogEntry } from '../App';

interface SleepStatsProps {
  logs: SleepLogEntry[];
}

export function SleepStats({ logs }: SleepStatsProps) {
  if (logs.length === 0) {
    return (
      <div className="space-y-6">
        {/* Hero Image for Empty State */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl overflow-hidden shadow-2xl">
          <div className="relative h-48">
            <img 
              src="https://images.unsplash.com/photo-1585817934451-158d9f444228?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzdW5yaXNlJTIwbW9ybmluZyUyMGxpZ2h0fGVufDF8fHx8MTc2NTM1NTU5NHww&ixlib=rb-4.1.0&q=80&w=1080"
              alt="Morning Light"
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
            <h2 className="absolute bottom-4 left-6 text-white text-2xl flex items-center gap-2">
              <BarChart size={24} />
              Statistik Tidur
            </h2>
          </div>
          
          <div className="p-6 text-center py-12">
            <TrendingUp size={48} className="text-white/30 mx-auto mb-4" />
            <p className="text-white/60">Belum ada data untuk statistik</p>
            <p className="text-white/40 text-sm mt-2">
              Catat tidur Anda setidaknya 3 kali untuk melihat statistik
            </p>
          </div>
        </div>
      </div>
    );
  }

  const totalSleep = logs.reduce((sum, log) => sum + log.duration, 0);
  const avgSleep = totalSleep / logs.length;
  const avgHours = Math.floor(avgSleep / 60);
  const avgMinutes = Math.floor(avgSleep % 60);

  const avgQuality = logs.filter(log => log.quality).length > 0
    ? logs.reduce((sum, log) => sum + (log.quality || 0), 0) / logs.filter(log => log.quality).length
    : 0;

  const longestSleep = Math.max(...logs.map(log => log.duration));
  const shortestSleep = Math.min(...logs.map(log => log.duration));

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = Math.floor(minutes % 60);
    return `${hours}j ${mins}m`;
  };

  // Calculate consistency score (based on standard deviation)
  const mean = avgSleep;
  const variance = logs.reduce((sum, log) => sum + Math.pow(log.duration - mean, 2), 0) / logs.length;
  const stdDev = Math.sqrt(variance);
  const consistencyScore = Math.max(0, Math.min(100, 100 - (stdDev / 60) * 10));

  return (
    <div className="space-y-6">
      {/* Hero Image Section */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl overflow-hidden shadow-2xl">
        <div className="relative h-48">
          <img 
            src="https://images.unsplash.com/photo-1585817934451-158d9f444228?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxzdW5yaXNlJTIwbW9ybmluZyUyMGxpZ2h0fGVufDF8fHx8MTc2NTM1NTU5NHww&ixlib=rb-4.1.0&q=80&w=1080"
            alt="Morning Light"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          <div className="absolute bottom-4 left-6">
            <h2 className="text-white text-2xl flex items-center gap-2 mb-1">
              <BarChart size={24} />
              Statistik Tidur
            </h2>
            <p className="text-white/80 text-sm">Analisis pola tidur Anda</p>
          </div>
        </div>
        
        {/* Overview Stats */}
        <div className="p-6">
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-gradient-to-br from-cyan-400/20 to-blue-500/20 rounded-lg p-4 text-center">
              <Moon size={32} className="text-cyan-400 mx-auto mb-2" />
              <p className="text-white/70 text-sm mb-1">Rata-rata Tidur</p>
              <p className="text-white text-2xl">{avgHours}j {avgMinutes}m</p>
            </div>

            <div className="bg-gradient-to-br from-yellow-400/20 to-orange-500/20 rounded-lg p-4 text-center">
              <Award size={32} className="text-yellow-400 mx-auto mb-2" />
              <p className="text-white/70 text-sm mb-1">Kualitas Rata-rata</p>
              <p className="text-white text-2xl">{avgQuality.toFixed(1)} ⭐</p>
            </div>

            <div className="bg-white/10 rounded-lg p-4 text-center">
              <p className="text-white/70 text-sm mb-1">Total Malam</p>
              <p className="text-white text-2xl">{logs.length}</p>
            </div>

            <div className="bg-white/10 rounded-lg p-4 text-center">
              <p className="text-white/70 text-sm mb-1">Konsistensi</p>
              <p className="text-cyan-400 text-2xl">{consistencyScore.toFixed(0)}%</p>
            </div>
          </div>

          <div className="space-y-3">
            <div className="bg-white/10 rounded-lg p-4 flex justify-between items-center">
              <span className="text-white/80">Tidur Terlama</span>
              <span className="text-green-400">{formatDuration(longestSleep)}</span>
            </div>
            <div className="bg-white/10 rounded-lg p-4 flex justify-between items-center">
              <span className="text-white/80">Tidur Terpendek</span>
              <span className="text-orange-400">{formatDuration(shortestSleep)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Trends */}
      <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 shadow-2xl">
        <h2 className="text-white text-xl mb-6 flex items-center gap-2">
          <TrendingUp size={24} />
          Tren 7 Hari Terakhir
        </h2>

        <div className="space-y-2">
          {logs.slice(0, 7).map((log, index) => {
            const percentage = (log.duration / (8 * 60)) * 100;
            return (
              <div key={log.id} className="space-y-1">
                <div className="flex justify-between text-sm">
                  <span className="text-white/70">
                    {new Date(log.date).toLocaleDateString('id-ID', { 
                      month: 'short', 
                      day: 'numeric' 
                    })}
                  </span>
                  <span className="text-white">{formatDuration(log.duration)}</span>
                </div>
                <div className="bg-white/20 rounded-full h-3 overflow-hidden">
                  <div 
                    className="bg-gradient-to-r from-cyan-400 to-blue-500 h-full rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(percentage, 100)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-4 p-4 bg-cyan-400/10 rounded-lg border border-cyan-400/30">
          <p className="text-white/80 text-sm">
            <strong className="text-cyan-400">Tips:</strong> Dewasa disarankan tidur 7-9 jam per malam untuk kesehatan optimal.
          </p>
        </div>
      </div>
    </div>
  );
}
