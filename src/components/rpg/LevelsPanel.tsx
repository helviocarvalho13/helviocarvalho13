import { motion } from "framer-motion";
import { projects } from "@/data/skills";

const LevelsPanel = () => {
  return (
    <div className="smw-panel p-2 h-full flex flex-col">
      <div className="border-b-2 border-smw-panel-border/30 pb-2 mb-2 flex items-center justify-between">
        <h2 className="font-pixel text-[7px] sm:text-[9px] text-primary smw-text-shadow">
          🏆 LEVELS
        </h2>
        <span className="font-pixel text-[5px] text-muted-foreground smw-text-shadow">
          PROJETOS
        </span>
      </div>

      <div className="grid grid-cols-3 gap-2 flex-1 content-start overflow-y-auto">
        {projects.map((project, i) => (
          <motion.div
            key={project.id}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: i * 0.06 }}
            className="smw-panel p-2 flex flex-col items-center gap-1 hover:bg-smw-panel-border/10 transition-colors cursor-default group"
            title={project.description}
          >
            <div className="relative">
              <span className="text-xl sm:text-2xl group-hover:scale-110 transition-transform inline-block">
                {project.icon}
              </span>
              <span className="absolute -top-1 -right-2 font-pixel text-[7px] sm:text-[9px] text-primary smw-text-shadow font-bold">
                {project.id}
              </span>
            </div>
            {/* Stars */}
            <div className="flex gap-0.5">
              {[1, 2, 3].map(s => (
                <span
                  key={s}
                  className={`text-[8px] sm:text-[10px] ${s <= project.stars ? "opacity-100" : "opacity-25"}`}
                >
                  ⭐
                </span>
              ))}
            </div>
            <span className="font-pixel text-[3px] sm:text-[4px] text-foreground smw-text-shadow text-center leading-tight">
              {project.name}
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default LevelsPanel;
