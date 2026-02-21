import { totalXP, maxXP, ceoInfo } from "@/data/skills";

const HUD = () => {
  const level = Math.floor(totalXP / 15);
  const xpPercent = Math.round((totalXP / maxXP) * 100);
  const coins = totalXP;

  return (
    <header className="fixed top-0 left-0 right-0 z-50 smw-panel p-2 sm:p-3">
      <div className="flex items-center justify-between gap-2 text-[7px] sm:text-[9px]">
        {/* Player info */}
        <div className="flex items-center gap-2">
          <span className="text-lg">🎮</span>
          <div>
            <p className="text-primary smw-text-shadow font-pixel">{ceoInfo.name.split(" ")[0].toUpperCase()}</p>
            <p className="text-muted-foreground font-pixel text-[5px] sm:text-[6px]">WORLD {ceoInfo.worldsExplored}</p>
          </div>
        </div>

        {/* Coins / XP */}
        <div className="flex items-center gap-1.5">
          <span className="text-sm animate-star-spin">⭐</span>
          <span className="text-primary smw-text-shadow font-pixel">×{coins}</span>
        </div>

        {/* Level */}
        <div className="text-center">
          <p className="text-primary smw-text-shadow font-pixel">LV.{level}</p>
          <div className="flex items-center gap-1 mt-0.5">
            <div className="w-16 sm:w-24 h-2.5 bg-smw-xp-bg border border-smw-panel-border relative overflow-hidden">
              <div
                className="h-full bg-smw-xp-bar transition-all duration-1000 relative"
                style={{ width: `${xpPercent}%` }}
              >
                <div className="absolute inset-0 xp-bar-shimmer" />
              </div>
            </div>
            <span className="text-muted-foreground font-pixel text-[5px]">{xpPercent}%</span>
          </div>
        </div>

        {/* Links */}
        <div className="hidden sm:flex items-center gap-3">
          <a
            href={ceoInfo.linkedin}
            target="_blank"
            rel="noopener noreferrer"
            className="font-pixel text-[6px] text-secondary hover:text-primary transition-colors smw-text-shadow"
          >
            LinkedIn
          </a>
          <a
            href={ceoInfo.companyUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="font-pixel text-[6px] text-secondary hover:text-primary transition-colors smw-text-shadow"
          >
            Luna Tech
          </a>
        </div>
      </div>
    </header>
  );
};

export default HUD;
