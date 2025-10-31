import { motion } from "framer-motion";

const animation = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -20 },
    transition: { duration: 0.4, ease: "easeOut" },
};

const AnimatedPageWrapper = ({ children }) => {
    return (
        <motion.div
            initial={animation.initial}
            animate={animation.animate}
            exit={animation.exit}
            transition={animation.transition}
        >
            {children}
        </motion.div>
    );
};

export default AnimatedPageWrapper;