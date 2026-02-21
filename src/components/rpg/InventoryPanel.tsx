import { motion, AnimatePresence } from "framer-motion";
import type { Region } from "@/data/skills";

interface InventoryPanelProps {
  region: Region | null;
}

const InventoryPanel = ({ region }: InventoryPanelProps) => {
  return (
    <div className="smw-panel p-2 h-full flex flex-col">
      <div className="border-b-2 border-smw-panel-border/30 pb-2 mb-2 flex items-center justify-between">
        <h2 className="font-pixel text-[7px] sm:text-[9px] text-primary smw-text-shadow">
          📦 INVENTORY
        </h2>
        {region && (
          <span className="font-pixel text-[5px] sm:text-[6px] text-muted-foreground smw-text-shadow">
            {region.emoji} {region.name}
          </span>
        )}
      </div>

      <AnimatePresence mode="wait">
        {region ? (
          <motion.div
            key={region.id}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="grid grid-cols-3 sm:grid-cols-4 gap-2 flex-1 content-start"
          >
            {region.skills.map((skill, i) => {
              const percent = Math.round((skill.projects / skill.maxProjects) * 100);
              return (
                <motion.div
                  key={skill.name}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.04 }}
                  className="smw-panel p-2 flex flex-col items-center gap-1 hover:bg-smw-panel-border/10 transition-colors cursor-default group"
                  title={`${skill.name}: ${skill.projects}/${skill.maxProjects} projetos`}
                >
                  <span className="text-xl sm:text-2xl group-hover:scale-110 transition-transform">
                    {skill.icon}
                  </span>
                  <span className="font-pixel text-[4px] sm:text-[5px] text-foreground smw-text-shadow text-center leading-tight">
                    {skill.name}
                  </span>
                  {/* Mini XP bar */}
                  <div className="w-full h-1.5 bg-smw-xp-bg border border-smw-panel-border/50 overflow-hidden">
                    <motion.div
                      className="h-full bg-smw-xp-bar"
                      initial={{ width: 0 }}
                      animate={{ width: `${percent}%` }}
                      transition={{ duration: 0.5, delay: i * 0.04 + 0.1 }}
                    />
                  </div>
                  <span className="font-pixel text-[3px] sm:text-[4px] text-muted-foreground">
                    {skill.projects}/{skill.maxProjects}
                  </span>
                </motion.div>
              );
            })}
          </motion.div>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex-1 flex items-center justify-center"
          >
            <p className="font-pixel text-[6px] sm:text-[7px] text-muted-foreground smw-text-shadow text-center">
              👈 Selecione uma<br />categoria de skills
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default InventoryPanel;
