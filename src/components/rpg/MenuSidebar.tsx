import { motion } from "framer-motion";
import type { Region } from "@/data/skills";

interface MenuSidebarProps {
  regions: Region[];
  selectedRegion: Region | null;
  onSelectRegion: (region: Region) => void;
}

const MenuSidebar = ({ regions, selectedRegion, onSelectRegion }: MenuSidebarProps) => {
  return (
    <div className="smw-panel p-2 flex flex-col gap-1 w-full">
      <div className="border-b-2 border-smw-panel-border/30 pb-2 mb-1">
        <h2 className="font-pixel text-[7px] sm:text-[9px] text-primary smw-text-shadow text-center">
          ⚔️ SKILLS ⚔️
        </h2>
      </div>
      {regions.map((region, i) => (
        <motion.button
          key={region.id}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: i * 0.05 }}
          onClick={() => onSelectRegion(region)}
          className={`
            w-full text-left px-3 py-2 font-pixel text-[6px] sm:text-[7px]
            border-2 transition-all duration-150
            ${selectedRegion?.id === region.id
              ? "bg-smw-node-bg/30 border-smw-panel-border text-primary smw-text-shadow scale-[1.02]"
              : "bg-transparent border-transparent text-foreground hover:bg-smw-panel-border/10 hover:border-smw-panel-border/30"
            }
          `}
        >
          <span className="mr-2">{region.emoji}</span>
          {region.name.toUpperCase()}
        </motion.button>
      ))}
    </div>
  );
};

export default MenuSidebar;
