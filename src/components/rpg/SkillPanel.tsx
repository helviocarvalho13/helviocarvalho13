import { motion, AnimatePresence } from "framer-motion";
import type { Region } from "@/data/skills";

interface SkillPanelProps {
  region: Region | null;
  onClose: () => void;
}

const SkillPanel = ({ region, onClose }: SkillPanelProps) => {
  return (
    <AnimatePresence>
      {region && (
        <motion.div
          initial={{ y: "100%", opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          exit={{ y: "100%", opacity: 0 }}
          transition={{ type: "spring", damping: 22, stiffness: 250 }}
          className="fixed bottom-0 left-0 right-0 z-40 smw-panel max-h-[60vh] overflow-y-auto"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-3 sm:p-4 border-b-2 border-smw-panel-border/30">
            <div className="flex items-center gap-3">
              <span className="text-2xl">{region.emoji}</span>
              <div>
                <h2 className="font-pixel text-[9px] sm:text-[11px] text-primary smw-text-shadow">
                  {region.name}
                </h2>
                <p className="font-pixel text-[6px] text-muted-foreground smw-text-shadow mt-0.5">
                  {region.description}
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="font-pixel text-xs text-muted-foreground hover:text-accent transition-colors smw-text-shadow px-2"
            >
              ✕
            </button>
          </div>

          {/* Skills grid */}
          <div className="p-3 sm:p-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {region.skills.map((skill, i) => {
              const percent = Math.round((skill.projects / skill.maxProjects) * 100);
              return (
                <motion.div
                  key={skill.name}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.06 }}
                  className="smw-panel p-3"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{skill.icon}</span>
                      <span className="font-pixel text-[7px] sm:text-[8px] text-foreground smw-text-shadow">
                        {skill.name}
                      </span>
                    </div>
                    <span className="font-pixel text-[6px] text-primary smw-text-shadow">
                      {skill.projects}/{skill.maxProjects}
                    </span>
                  </div>

                  {/* XP Bar */}
                  <div className="w-full h-3 bg-smw-xp-bg border border-smw-panel-border/50 relative overflow-hidden">
                    <motion.div
                      className="h-full bg-smw-xp-bar relative"
                      initial={{ width: 0 }}
                      animate={{ width: `${percent}%` }}
                      transition={{ duration: 0.6, delay: i * 0.06 + 0.15 }}
                    >
                      {percent >= 80 && (
                        <div className="absolute inset-0 xp-bar-shimmer" />
                      )}
                    </motion.div>
                  </div>

                  <div className="flex justify-between mt-1">
                    <span className="font-pixel text-[5px] text-muted-foreground">
                      {percent}% EXP
                    </span>
                    {percent >= 90 && (
                      <span className="font-pixel text-[5px] text-primary smw-text-shadow">
                        ⭐ MASTER
                      </span>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default SkillPanel;
